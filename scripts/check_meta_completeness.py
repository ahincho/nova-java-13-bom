#!/usr/bin/env python3
"""Prueba de completitud de las meta-dependencias de Nova (ADR-052, regla 2).

El meta-starter de Spring Boot (`nova-spring-boot-starter`) y la meta-extensión de Quarkus
(`nova-quarkus-extension`) traen las demás piezas del nivel 2 para que un servicio declare una sola
dependencia. El BOM es el único lugar que las conoce todas, así que aquí vive la prueba: cada
`*-spring-boot-starter` o `*-quarkus-extension` que el BOM gestiona tiene que estar declarado por la
meta-dependencia, en la misma versión.

La meta-dependencia se lee del POM que está publicado en GitHub Packages, en la versión que el BOM
gestiona. Por eso el orden de publicación es fijo (ADR-052, regla 3): sale el artefacto, después la
meta-dependencia que lo trae y por último el BOM. Si el BOM sale antes, esta prueba lo frena.

Uso local (el token necesita el permiso read:packages):

    GITHUB_TOKEN=$(gh auth token --user ahincho) python3 scripts/check_meta_completeness.py

Termina con 0 si todo está completo, con 1 si falta algo o hay una versión distinta, y con 2 si no
pudo leer lo que tenía que comprobar.
"""

from __future__ import annotations

import base64
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

POM = "{http://maven.apache.org/POM/4.0.0}"
STARTERS_GROUP = "pe.edu.nova.java.starters"
# Para leer, GitHub Packages solo mira el dueño: cualquier repositorio de ahincho sirve de ruta.
DEFAULT_REGISTRY = "https://maven.pkg.github.com/ahincho/nova-java-13-bom"


@dataclass(frozen=True)
class Family:
    """Un BOM y la meta-dependencia que tiene que traer todo lo que él gestiona."""

    name: str
    bom_pom: str  # ruta del POM del BOM, desde la raíz del repositorio
    meta: str  # artifactId de la meta-dependencia
    suffix: str  # lo que identifica a los miembros: `*-spring-boot-starter`, `*-quarkus-extension`
    required: bool  # si el BOM tiene que gestionar ya la meta-dependencia
    # Lo que el BOM gestiona y la meta-dependencia deja fuera a propósito: artifactId -> por qué.
    # Una exclusión que ya no aplica rompe la prueba, para que la lista no se quede vieja.
    excluded: dict[str, str] = field(default_factory=dict)


FAMILIES = [
    Family(
        name="Spring Boot",
        bom_pom="nova-spring-boot-bom/pom.xml",
        meta="nova-spring-boot-starter",
        suffix="-spring-boot-starter",
        required=True,
        excluded={
            "nova-idempotency-spring-boot-starter": (
                "enmienda de ADR-052: se enciende sola, exige la tabla de su almacén JDBC y es 0.x; "
                "entra cuando no cambie nada sin configurarla, en una versión 1.x"
            ),
        },
    ),
    Family(
        name="Quarkus",
        bom_pom="nova-quarkus-bom/pom.xml",
        meta="nova-quarkus-extension",
        suffix="-quarkus-extension",
        # La meta-extensión (repositorio nova-java-26-quarkus-extension, ADR-052, paso 2) todavía no
        # existe. En cuanto nova-quarkus-bom la gestione, la prueba corre sola; ahí conviene pasar
        # esto a True para que quitarla del BOM no apague la prueba en silencio.
        required=False,
    ),
]


class CheckError(Exception):
    """No se pudo hacer la comprobación: falta el token, el POM no está publicado, no hay red."""


def _text(element: ET.Element, tag: str) -> str | None:
    child = element.find(POM + tag)
    return child.text.strip() if child is not None and child.text else None


def _resolve(value: str | None, root: ET.Element) -> str | None:
    """Reemplaza `${propiedad}` por lo que declara el mismo POM. Lo que no encuentra se deja igual."""
    if value is None:
        return None
    properties = root.find(POM + "properties")
    children = properties if properties is not None else []
    known = {child.tag.removeprefix(POM): (child.text or "").strip() for child in children}
    for _ in range(10):  # una propiedad puede apuntar a otra
        expanded = re.sub(r"\$\{([^}]+)\}", lambda m: known.get(m.group(1), m.group(0)), value)
        if expanded == value:
            break
        value = expanded
    return value


def managed_starters(bom_xml: bytes | str) -> dict[str, str]:
    """Lo que un BOM gestiona en el grupo de los starters: artifactId -> versión resuelta."""
    root = ET.fromstring(bom_xml)
    managed = {}
    for dependency in root.findall(f"{POM}dependencyManagement/{POM}dependencies/{POM}dependency"):
        if _text(dependency, "groupId") != STARTERS_GROUP:
            continue
        artifact = _text(dependency, "artifactId")
        version = _resolve(_text(dependency, "version"), root)
        if version is None or "${" in version:
            raise CheckError(f"el BOM gestiona {artifact} con una versión que no se resuelve: {version}")
        managed[artifact] = version
    return managed


def declared_dependencies(pom_xml: bytes | str) -> dict[str, str | None]:
    """Lo que un POM declara en el grupo de los starters: artifactId -> versión, o None si no la lleva."""
    root = ET.fromstring(pom_xml)
    return {
        _text(dependency, "artifactId"): _resolve(_text(dependency, "version"), root)
        for dependency in root.findall(f"{POM}dependencies/{POM}dependency")
        if _text(dependency, "groupId") == STARTERS_GROUP
    }


def check_family(
    family: Family,
    managed: dict[str, str],
    fetch_pom: Callable[[str, str], bytes | str],
    out: Callable[[str], None] = print,
) -> list[str]:
    """Compara lo que el BOM gestiona con lo que declara la meta-dependencia; devuelve las fallas."""
    if family.meta not in managed:
        if family.required:
            return [f"{family.name}: el BOM tiene que gestionar {family.meta} y no lo hace"]
        out(
            f"== {family.name}: {family.bom_pom} todavía no gestiona {family.meta} (ADR-052, paso 3). "
            "No hay meta-dependencia que comprobar: la prueba pasa."
        )
        return []

    meta, meta_version = family.meta, managed[family.meta]
    out(f"== {family.name}: {meta} {meta_version} contra lo que gestiona {family.bom_pom}")
    declared = declared_dependencies(fetch_pom(meta, meta_version))
    failures: list[str] = []

    def fail(message: str) -> None:
        failures.append(message)
        out(f"   FALLA   {message}")

    members = sorted(a for a in managed if a.endswith(family.suffix) and a != meta)
    for artifact in members:
        expected, actual = managed[artifact], declared.get(artifact)
        if artifact in family.excluded:
            if artifact in declared:
                fail(f"{artifact} está excluido pero {meta} ya lo declara: sacarlo de la lista de exclusiones")
            else:
                out(f"   fuera   {artifact} ({family.excluded[artifact]})")
        elif artifact not in declared:
            fail(f"{artifact}: el BOM gestiona la {expected} y {meta} {meta_version} no lo declara")
        elif actual is None:
            fail(f"{artifact}: {meta} lo declara sin versión, y la regla 1 de ADR-052 pide la versión explícita")
        elif actual != expected:
            fail(f"{artifact}: el BOM gestiona la {expected} y {meta} {meta_version} declara la {actual}")
        else:
            out(f"   ok      {artifact} {expected}")

    for artifact in sorted(set(family.excluded) - set(members)):
        fail(f"{artifact} está excluido pero el BOM ya no lo gestiona: sacarlo de la lista de exclusiones")
    return failures


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # la redirección se sigue a mano, para no mandar el token al destino


def _download(url: str, headers: dict[str, str]) -> bytes:
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.build_opener(_NoRedirect).open(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        # GitHub Packages contesta con una redirección a una URL firmada, que va sin credenciales.
        if error.code in (301, 302, 303, 307, 308) and error.headers.get("Location"):
            return _download(error.headers["Location"], {})
        raise


def fetch_published_pom(artifact: str, version: str) -> bytes:
    """El POM publicado de un starter o una extensión, leído de GitHub Packages."""
    registry = os.environ.get("NOVA_PACKAGES_URL", DEFAULT_REGISTRY)
    token = os.environ.get("NOVA_PACKAGES_READ_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise CheckError("falta un token con read:packages en NOVA_PACKAGES_READ_TOKEN o GITHUB_TOKEN")
    user = os.environ.get("GITHUB_ACTOR", "nova")
    credentials = base64.b64encode(f"{user}:{token}".encode()).decode()
    url = f"{registry}/{STARTERS_GROUP.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}.pom"
    for attempt in range(3):
        try:
            return _download(url, {"Authorization": f"Basic {credentials}"})
        except urllib.error.HTTPError as error:
            if error.code == 404:
                raise CheckError(
                    f"{artifact} {version} no está publicado. El orden es fijo (ADR-052, regla 3): primero "
                    "el artefacto, después la meta-dependencia que lo trae y por último el BOM"
                ) from None
            if error.code in (401, 403):
                raise CheckError(f"sin permiso para leer {artifact} {version} (HTTP {error.code})") from None
            problem = f"HTTP {error.code}"
        except urllib.error.URLError as error:
            problem = str(error.reason)
        if attempt < 2:
            time.sleep(2 * (attempt + 1))
    raise CheckError(f"no se pudo leer {url}: {problem}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parent.parent
    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    failures: list[str] = []
    try:
        for family in FAMILIES:
            managed = managed_starters((root / family.bom_pom).read_bytes())
            failures += check_family(family, managed, fetch_published_pom)
    except CheckError as error:
        print(f"ERROR: {error}")
        if in_actions:
            print(f"::error title=No se pudo comprobar la completitud::{error}")
        return 2
    if failures:
        print(f"\nLa prueba de completitud falló con {len(failures)} problema(s).")
        if in_actions:
            for failure in failures:
                print(f"::error title=Meta-dependencia incompleta::{failure}")
        return 1
    print("\nLa prueba de completitud pasó.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
