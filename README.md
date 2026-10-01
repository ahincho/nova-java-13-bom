# Nova Platform BOM

BOM (Bill of Materials) raíz que centraliza las versiones de las librerías y starters de **Nova Platform** (`pe.edu.nova.java`). Agnóstico al framework: expone un BOM puro (`nova-bom`) y BOMs específicos por stack (`nova-spring-boot-bom`, `nova-quarkus-bom`, `nova-micronaut-bom`).

## Matriz de compatibilidad

> Generada manualmente a partir del estado real publicado en GitHub Packages (no de `libs.versions.toml`: el proyecto no tiene un version catalog centralizado — ver "Cómo se mantiene esta matriz" más abajo). Última actualización: 2026-10-01 (ADR-041, ADR-047 y ADR-031).

### `nova-bom` (librerías puras Java, sin dependencia de ningún framework)

| `nova-bom` | `nova-api-standard` | `nova-date-utils` | `nova-mapper-utils` | `nova-mask-utils` |
|---|---|---|---|---|
| **1.0.0** | 1.0.0 | 1.0.0 | 1.0.0 | 1.0.0 |
| **2.0.0** | 1.0.2 | 1.0.2 | 1.0.2 | 1.1.2 |
| **2.0.1** | 1.0.2 | 1.0.2 | 1.0.2 | 1.1.2 |
| **2.0.2** | 1.0.2 | 1.0.2 | 1.0.2 | 1.1.2 |
| **2.0.3** | 1.0.2 | 1.0.2 | 1.0.2 | 1.1.2 |
| **2.1.0** | 1.0.2 | 1.0.2 | 1.0.2 | 1.1.2 |
| **2.2.0** | 1.0.2 | 1.0.2 | 1.0.2 | 1.1.2 |
| **3.0.0** | 1.1.0 | 1.0.2 | 1.0.2 | 1.1.2 |

### `nova-spring-boot-bom` (extiende `nova-bom` + Spring Boot)

| `nova-spring-boot-bom` | Spring Boot | `nova-spring-boot-starter` | `nova-api-standard-spring-boot-starter` | `nova-mask-spring-boot-starter` | `nova-observability-spring-boot-starter` | familia `nova-secrets` | familia `nova-idempotency` |
|---|---|---|---|---|---|---|---|
| **1.0.0** | 4.0.5 | 1.0.0 | 1.0.0 | 1.0.0 | 1.0.0 | - | - |
| **2.0.0** | 4.0.8, con Tomcat 11.0.26 | 1.0.3 | 2.0.0 | 2.0.0 | 2.0.0 | - | - |
| **2.0.1** | 4.0.8, con Tomcat 11.0.26 | 1.0.3 | 2.0.0 | 2.0.0 | 2.0.0 | - | - |
| **2.0.2** | 4.0.8, con Tomcat 11.0.26 | 1.0.3 | 2.0.0 | 2.0.0 | 2.0.1 | - | - |
| **2.0.3** | 4.0.8, con Tomcat 11.0.26 y OpenTelemetry 1.65.0 | 1.0.4 | 2.0.0 | 2.0.0 | 2.0.1 | - | - |
| **2.1.0** | 4.0.8, con Tomcat 11.0.26 y OpenTelemetry 1.65.0 | 1.0.4 | 2.0.0 | 2.0.0 | 2.0.2 | 1.0.1 | - |
| **2.2.0** | 4.0.8, con Tomcat 11.0.26 y OpenTelemetry 1.65.0 | 1.0.4 | 2.0.0 | 2.0.0 | 2.0.2 | 1.0.1 | 0.1.1 |
| **3.0.0** | 4.0.8, con Tomcat 11.0.26 y OpenTelemetry 1.65.0 | 1.0.4 | 3.0.0 | 3.0.0 | 2.0.2 | 1.0.1 | 0.1.1 |

Hasta la 1.0.x, los tres starters se publicaban como `nova-api-standard-starter`, `nova-mask-starter` y `nova-observability-starter`. La 2.0.0 del BOM gestiona los nombres de [ADR-039](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/shared/ADR-039-nombres-de-artefacto-derivados-del-repositorio.md), y fija Tomcat en 11.0.26 porque Spring Boot 4.0.8 todavía trae la 11.0.24, con tres CVE altos. La 2.0.1 quiso pasar `nova-spring-boot-starter` a la 1.0.4, que reexporta los starters con los nombres nuevos, pero solo cambió una propiedad que la entrada no usa: la 2.0.1 y la 2.0.2 siguieron gestionando la 1.0.3. La 2.0.2 pasa `nova-observability-spring-boot-starter` a la 2.0.1, porque la 2.0.0 no resuelve: pide `opentelemetry-semconv-incubating` 1.43.0, una versión que no existe. La 2.0.3 gestiona por fin `nova-spring-boot-starter` 1.0.4 e importa `opentelemetry-instrumentation-bom` 2.31.1 antes que Spring Boot. Sin ese import, en Maven el núcleo de OpenTelemetry queda en la 1.55.0 que fija Spring Boot 4.0.8, y el starter de observabilidad, construido con la instrumentación 2.31.1, falla al arrancar con `NoSuchFieldError`. La 2.1.0 suma la familia `nova-secrets` en la 1.0.1, que se explica más abajo, y pasa `nova-observability-spring-boot-starter` a la 2.0.2, construida sobre Spring Boot 4.0.8 como el resto de la plataforma. La 2.2.0 suma la familia `nova-idempotency` en la 0.1.1. La 3.0.0 gestiona el modelo de errores por capas de [ADR-031](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/shared/ADR-031-modulo-de-errores-por-capas-con-trazabilidad.md): `nova-api-standard` 1.1.0 y los dos starters de `nova-java-08-commons-spring-boot-starter` en la 3.0.0. Es mayor porque la 3.0.0 del starter de API cambia lo que un cliente recibe ante un error; la receta está más abajo.

**Migrar a la 3.0.0.** Para un servicio que solo sube la versión del BOM, el cambio está en las respuestas de error. La receta completa está en [«Migrating to 3.0.0»](https://github.com/ahincho/nova-java-08-commons-spring-boot-starter#migrating-to-300) del starter; en resumen:

| Antes (2.x) | Desde la 3.0.0 | Qué hacer |
|---|---|---|
| el código `ERROR` en un error lanzado | el código del catálogo según el status, o el código propio del error | comparar contra el código del catálogo |
| `VALIDATION_ERROR` en la validación | `BAD_REQUEST`, con los mismos errores por campo | comparar contra `BAD_REQUEST` |
| `IllegalArgumentException` respondida como 400 | un `PlatformError`, respondido como 500 | lanzar `ApplicationError.invalidInput(...)` ante una entrada inválida |
| mensajes genéricos en inglés, como `Not Found` | los mensajes del catálogo en español | no comparar contra el texto del mensaje |
| `ErrorCodes` y `GlobalExceptionHandler.envelope(...)` | eliminados | usar `NovaErrorCatalog.platformCode(status)` o el bean `ErrorPorts` |

`nova-mask-spring-boot-starter` pasa a la 3.0.0 solo porque el repositorio publica sus dos starters con una sola versión: no cambia nada para quien lo usa. `nova-spring-boot-starter` sigue en la 1.0.4, y con este BOM resuelve los starters en la 3.0.0. La extensión de Quarkus sigue en la 2.0.1: `nova-api-standard` 1.1.0 solo agrega API, así que la acepta sin cambios.

⚠️ **Importante — alcance real de `nova-spring-boot-bom` para consumidores Maven:** este BOM gestiona directamente los 4 starters + `spring-boot-dependencies`, pero **NO** re-importa (`<scope>import</scope>`) las 4 librerías puras de `nova-bom` (`nova-api-standard`, `nova-date-utils`, `nova-mapper-utils`, `nova-mask-utils`) — solo las obtiene por herencia normal de `<parent>`. Esto tiene una consecuencia real y no obvia:
- **Consumidores Gradle** (via `api(platform("pe.edu.nova.java:nova-spring-boot-bom:3.0.0"))`): SÍ ven las 4 librerías gestionadas, porque Gradle lee el modelo POM efectivo completo (incluyendo lo heredado del `<parent>`). Así es como `nova-spring-boot-starter` declara `api("pe.edu.nova.java.libs:nova-date-utils")` sin versión y funciona.
- **Consumidores Maven** que importen `nova-spring-boot-bom` con `<scope>import</scope>` (la forma estándar/correcta de consumir un BOM en Maven) **NO** heredan la gestión de versiones de las 4 librerías puras — Maven's `import` scope solo trae el `<dependencyManagement>` propio del POM importado, no el de sus padres transitivos. Si necesitas una versión gestionada de `nova-date-utils` en un proyecto Maven, importa **también** `nova-bom` explícitamente, o fija la versión manualmente.

**Familia `nova-secrets`.** Desde la 2.1.0, este BOM gestiona la familia `nova-secrets` en la 1.0.1 ([ADR-041](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/java/ADR-041-un-repositorio-por-capacidad.md)): las librerías `nova-secrets`, `nova-secrets-vault` y `nova-secrets-aws-secrets-manager` (`pe.edu.nova.java.libs`) y el starter `nova-secrets-spring-boot-starter` (`pe.edu.nova.java.starters`). `nova-java-23-secrets` publica los cuatro con una sola versión, así que el BOM los gestiona con una sola propiedad, `nova-secrets.version`. A diferencia de las cuatro librerías puras de `nova-bom`, las tres librerías de la familia sí llegan a los consumidores Maven que importan este BOM, porque están en su propio `dependencyManagement`. Solo este BOM la gestiona: secretos no tiene conector de Quarkus ni de Micronaut.

**Familia `nova-idempotency`.** Desde la 2.2.0, este BOM gestiona la familia `nova-idempotency` en la 0.1.1 ([ADR-047](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/shared/ADR-047-idempotencia-detras-de-un-contrato.md)): las librerías `nova-idempotency` y `nova-idempotency-jdbc` (`pe.edu.nova.java.libs`) y el starter `nova-idempotency-spring-boot-starter` (`pe.edu.nova.java.starters`), con una sola propiedad, `nova-idempotency.version`, igual que secretos. Todavía es 0.x: la 1.0.0 llega cuando pedidos de Plaza valide la API. La extensión de Quarkus llega con su primer consumidor.

### `nova-quarkus-bom` (extiende `nova-bom` + Quarkus)

| `nova-quarkus-bom` | Quarkus | `nova-api-standard-quarkus-extension` |
|---|---|---|
| **2.0.0** | 3.33.3.3 LTS | 2.0.1 |
| **2.0.1** | 3.33.3.3 LTS | 2.0.1 |
| **2.0.2** | 3.33.3.3 LTS | 2.0.1 |
| **2.0.3** | 3.33.3.3 LTS | 2.0.1 |
| **2.1.0** | 3.33.3.3 LTS | 2.0.1 |
| **2.2.0** | 3.33.3.3 LTS | 2.0.1 |
| **3.0.0** | 3.33.3.3 LTS | 2.0.1 |

Hasta la 1.0.2, este BOM pedía `nova-quarkus-api-ext:1.0.1`, un paquete que ya no existe en el registro, así que no resolvía.

### `nova-micronaut-bom`

Importa `micronaut-platform` 5.0.4 y todavía no gestiona ningún artefacto de Nova.

## Cómo consumir

### Maven

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>pe.edu.nova.java</groupId>
      <artifactId>nova-spring-boot-bom</artifactId>
      <version>3.0.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
    <!-- Si tu proyecto usa alguna libreria pura directamente (no solo starters),
         importa tambien el BOM raiz -->
    <dependency>
      <groupId>pe.edu.nova.java</groupId>
      <artifactId>nova-bom</artifactId>
      <version>3.0.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

GitHub Packages requiere autenticación incluso para lectura pública — ver [`nova-java-spring-boot-parent/pom.xml`](https://github.com/ahincho/nova-java-14-spring-boot-parent/blob/main/pom.xml) para un ejemplo de `<repositories>` + `settings.xml` (server id por repo Nova externo, ya que Maven exige `id` único por `<repository>`).

### Gradle

```kotlin
dependencies {
    api(platform("pe.edu.nova.java:nova-spring-boot-bom:3.0.0"))
    api("pe.edu.nova.java.libs:nova-date-utils") // version gestionada por el BOM
}

repositories {
    maven {
        url = uri("https://maven.pkg.github.com/ahincho/nova-java-13-bom")
        credentials {
            username = System.getenv("GITHUB_ACTOR")
            password = System.getenv("NOVA_PACKAGES_READ_TOKEN") ?: System.getenv("GITHUB_TOKEN")
        }
    }
}
```

## Compatibilidad de Java

Todos los artefactos de Nova Platform se validan en CI contra **Java 21** (mínimo) y **Java 25** (recomendado) — ver `reusable-build-matrix.yml` en `nova-devops` (NOVA-SEMVER-19).

## Known issues (2026-07-12)

| # | Artefacto | Problema | Estado |
|---|---|---|---|
| 1 | `nova-java-spring-boot-starter:1.0.0` | Su POM publicado referencia `nova-spring-boot-bom:1.0.1` — una versión que existió brevemente (workaround de un 409 Conflict, ver historial de versiones más abajo) y fue eliminada al revertir a `1.0.0`. El artefacto nunca se re-publicó tras el revert. **Efecto**: cualquier consumidor Maven que dependa directamente de este artefacto (hoy, solo `nova-java-spring-boot-parent`) no puede resolverlo. Los consumidores Gradle no se ven afectados de la misma forma porque no leen el `<dependencyManagement>` publicado de la misma manera. | Diagnosticado, requiere cortar una versión nueva (p.ej. `1.0.1`) — el código fuente ya es correcto, no hace falta cambiarlo. |
| 2 | `nova-java-spring-boot-parent`, `nova-java-spring-boot-archetype` | Ninguno de los 2 tiene workflow de publish (`publish.yml`/`publish-on-tag.yml`) — solo CI de validación (build/matrix/owasp/sbom). Nunca fueron publicados a GitHub Packages. Además, la plantilla del arquetipo (`archetype-resources/pom.xml`) referencia `nova-spring-boot-parent:0.1.0-SNAPSHOT`, que tampoco existe publicado en ningún lado — cualquier proyecto generado hoy con `mvn archetype:generate` fallaría al buildear. | Documentado, fuera de alcance de NOVA-SEMVER-22. Requiere configurar release-please para estos 2 repos. |

## Cómo se mantiene esta matriz

No existe un `gradle/libs.versions.toml` (version catalog) compartido entre los 9 repos Gradle — cada `build.gradle.kts` declara sus propias versiones de forma independiente. Esta tabla es **mantenida manualmente**: actualízala cada vez que se publique una versión nueva de cualquier BOM o de cualquier artefacto que un BOM gestione. Fuente de verdad para "qué está realmente publicado": tags Git (`v*`) + `.release-please-manifest.json` + `CHANGELOG.md` de cada repo — **no** el `gradle.properties`/`pom.xml` del working tree (que normalmente queda en `0.1.0-SNAPSHOT`/`-SNAPSHOT` entre releases).

Ver también: [ADR-018 — Política de versionado y bump](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/versioning/ADR-018-politica-de-versioning-y-bump.md), [docs/java/06-semantic-versioning-en-java.md](https://github.com/ahincho/nova-shared-01-docs/blob/main/java/06-semantic-versioning-en-java.md) (§11.9.30, NOVA-SEMVER-22).

## License

Eclipse Public License 2.0 — see [LICENSE](LICENSE).

Copyright © 2026 Angel Hincho.
