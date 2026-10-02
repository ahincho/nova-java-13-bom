"""Pruebas de check_meta_completeness.py, sin red: los POM son de mentira.

    python3 -m unittest discover -s scripts -v
"""

from __future__ import annotations

import unittest

from check_meta_completeness import (
    STARTERS_GROUP,
    CheckError,
    Family,
    check_family,
    declared_dependencies,
    managed_starters,
)

NS = 'xmlns="http://maven.apache.org/POM/4.0.0"'


def dependency(artifact: str, version: str | None = None, group: str = STARTERS_GROUP) -> str:
    tag = f"<version>{version}</version>" if version else ""
    return f"<dependency><groupId>{group}</groupId><artifactId>{artifact}</artifactId>{tag}</dependency>"


def bom(entries: list[str], properties: str = "") -> str:
    managed = f"<dependencyManagement><dependencies>{''.join(entries)}</dependencies></dependencyManagement>"
    return f"<project {NS}><properties>{properties}</properties>{managed}</project>"


def meta(entries: list[str]) -> str:
    return f"<project {NS}><dependencies>{''.join(entries)}</dependencies></project>"


SPRING = Family(
    name="Spring Boot",
    bom_pom="nova-spring-boot-bom/pom.xml",
    meta="nova-spring-boot-starter",
    suffix="-spring-boot-starter",
    required=True,
    excluded={"nova-idempotency-spring-boot-starter": "se enciende sola"},
)
QUARKUS = Family(
    name="Quarkus",
    bom_pom="nova-quarkus-bom/pom.xml",
    meta="nova-quarkus-extension",
    suffix="-quarkus-extension",
    required=False,
)

SPRING_BOM = bom(
    [
        dependency("nova-spring-boot-starter", "3.0.0"),
        dependency("nova-mask-spring-boot-starter", "4.0.0"),
        dependency("nova-secrets-spring-boot-starter", "${nova-secrets.version}"),
        dependency("nova-idempotency-spring-boot-starter", "0.1.1"),
        dependency("nova-secrets", "${nova-secrets.version}", group="pe.edu.nova.java.libs"),
    ],
    properties="<nova-secrets.version>1.2.0</nova-secrets.version>",
)


def run(family: Family, bom_xml: str, meta_xml: str | None = None):
    """Devuelve las fallas y las líneas del log. Si la prueba pidiera el POM del meta sin que haya, rompe."""

    def fetch(artifact: str, version: str) -> str:
        if meta_xml is None:
            raise AssertionError(f"no debía leer {artifact} {version}")
        return meta_xml

    lines: list[str] = []
    return check_family(family, managed_starters(bom_xml), fetch, lines.append), lines


class ReadingPoms(unittest.TestCase):
    def test_managed_versions_resolve_properties_and_keep_only_starters(self):
        managed = managed_starters(SPRING_BOM)
        self.assertEqual(managed["nova-secrets-spring-boot-starter"], "1.2.0")
        self.assertNotIn("nova-secrets", managed)

    def test_unresolvable_managed_version_stops_the_check(self):
        with self.assertRaises(CheckError):
            managed_starters(bom([dependency("nova-x-spring-boot-starter", "${missing}")]))

    def test_declared_dependency_without_version_is_none(self):
        declared = declared_dependencies(meta([dependency("nova-mask-spring-boot-starter")]))
        self.assertIsNone(declared["nova-mask-spring-boot-starter"])


class SpringBoot(unittest.TestCase):
    complete = meta(
        [
            dependency("nova-mask-spring-boot-starter", "4.0.0"),
            dependency("nova-secrets-spring-boot-starter", "1.2.0"),
        ]
    )

    def test_complete_meta_starter_passes_and_names_the_exclusion(self):
        failures, lines = run(SPRING, SPRING_BOM, self.complete)
        self.assertEqual(failures, [])
        self.assertTrue(any("fuera   nova-idempotency-spring-boot-starter" in line for line in lines))

    def test_missing_starter_fails(self):
        failures, _ = run(SPRING, SPRING_BOM, meta([dependency("nova-mask-spring-boot-starter", "4.0.0")]))
        self.assertEqual(len(failures), 1)
        self.assertIn("nova-secrets-spring-boot-starter", failures[0])
        self.assertIn("no lo declara", failures[0])

    def test_different_version_fails_and_names_both(self):
        stale = meta(
            [
                dependency("nova-mask-spring-boot-starter", "3.0.1"),
                dependency("nova-secrets-spring-boot-starter", "1.2.0"),
            ]
        )
        failures, _ = run(SPRING, SPRING_BOM, stale)
        self.assertEqual(len(failures), 1)
        self.assertIn("gestiona la 4.0.0", failures[0])
        self.assertIn("declara la 3.0.1", failures[0])

    def test_dependency_without_explicit_version_fails(self):
        versionless = meta(
            [dependency("nova-mask-spring-boot-starter"), dependency("nova-secrets-spring-boot-starter", "1.2.0")]
        )
        failures, _ = run(SPRING, SPRING_BOM, versionless)
        self.assertEqual(len(failures), 1)
        self.assertIn("sin versión", failures[0])

    def test_excluded_starter_that_the_meta_starter_now_declares_fails(self):
        declares_it = meta(
            [
                dependency("nova-mask-spring-boot-starter", "4.0.0"),
                dependency("nova-secrets-spring-boot-starter", "1.2.0"),
                dependency("nova-idempotency-spring-boot-starter", "0.1.1"),
            ]
        )
        failures, _ = run(SPRING, SPRING_BOM, declares_it)
        self.assertEqual(len(failures), 1)
        self.assertIn("ya lo declara", failures[0])

    def test_exclusion_for_a_starter_the_bom_no_longer_manages_fails(self):
        without_idempotency = bom(
            [dependency("nova-spring-boot-starter", "3.0.0"), dependency("nova-mask-spring-boot-starter", "4.0.0")]
        )
        failures, _ = run(SPRING, without_idempotency, meta([dependency("nova-mask-spring-boot-starter", "4.0.0")]))
        self.assertEqual(len(failures), 1)
        self.assertIn("ya no lo gestiona", failures[0])

    def test_the_meta_starter_is_not_its_own_member(self):
        failures, lines = run(SPRING, SPRING_BOM, self.complete)
        self.assertEqual(failures, [])
        self.assertFalse(any("ok      nova-spring-boot-starter" in line for line in lines))

    def test_bom_that_does_not_manage_the_meta_starter_fails(self):
        failures, _ = run(SPRING, bom([dependency("nova-mask-spring-boot-starter", "4.0.0")]))
        self.assertEqual(len(failures), 1)
        self.assertIn("tiene que gestionar nova-spring-boot-starter", failures[0])


class Quarkus(unittest.TestCase):
    def test_passes_with_a_log_line_while_the_bom_has_no_meta_extension(self):
        only_extensions = bom([dependency("nova-api-standard-quarkus-extension", "3.0.0")])
        failures, lines = run(QUARKUS, only_extensions)  # sin POM de meta: no debe leer nada
        self.assertEqual(failures, [])
        self.assertEqual(len(lines), 1)
        self.assertIn("todavía no gestiona nova-quarkus-extension", lines[0])
        self.assertIn("la prueba pasa", lines[0])

    def test_checks_every_extension_once_the_bom_manages_the_meta_extension(self):
        managed = bom(
            [
                dependency("nova-quarkus-extension", "0.1.0"),
                dependency("nova-api-standard-quarkus-extension", "3.0.0"),
                dependency("nova-secrets-quarkus-extension", "1.2.0"),
                dependency("nova-api-standard-quarkus-extension-deployment", "3.0.0"),
            ]
        )
        complete = meta(
            [
                dependency("nova-api-standard-quarkus-extension", "3.0.0"),
                dependency("nova-secrets-quarkus-extension", "1.2.0"),
            ]
        )
        failures, _ = run(QUARKUS, managed, complete)
        self.assertEqual(failures, [])

        stale = meta(
            [
                dependency("nova-api-standard-quarkus-extension", "2.0.1"),
                dependency("nova-secrets-quarkus-extension", "1.2.0"),
            ]
        )
        failures, _ = run(QUARKUS, managed, stale)
        self.assertEqual(len(failures), 1)
        self.assertIn("nova-api-standard-quarkus-extension", failures[0])

        missing = meta([dependency("nova-api-standard-quarkus-extension", "3.0.0")])
        failures, _ = run(QUARKUS, managed, missing)
        self.assertEqual(len(failures), 1)
        self.assertIn("nova-secrets-quarkus-extension", failures[0])


if __name__ == "__main__":
    unittest.main()
