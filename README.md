# Nova Platform BOM

BOM (Bill of Materials) raíz que centraliza las versiones de las librerías y starters de **Nova Platform** (`pe.edu.nova.java`). Agnóstico al framework: expone un BOM puro (`nova-bom`) y BOMs específicos por stack (`nova-spring-boot-bom`, `nova-quarkus-bom`, `nova-micronaut-bom`).

## Matriz de compatibilidad

> Generada manualmente a partir del estado real publicado en GitHub Packages (no de `libs.versions.toml`: el proyecto no tiene un version catalog centralizado — ver "Cómo se mantiene esta matriz" más abajo). Última actualización: 2026-10-01 (ADR-041, ADR-047, ADR-031 y ADR-052).

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
| **3.0.1** | 1.1.0 | 1.0.2 | 1.0.2 | 1.1.2 |
| **3.1.0** | 1.1.0 | 1.0.2 | 1.0.2 | 1.1.2 |
| **4.0.0** | 1.1.0 | 1.0.2 | 1.0.2 | 1.1.2 |

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
| **3.0.1** | 4.0.8, con Tomcat 11.0.26 y OpenTelemetry 1.65.0 | 1.0.4 | 3.0.1 | 3.0.1 | 2.0.2 | 1.0.1 | 0.1.1 |
| **3.1.0** | 4.0.8, con Tomcat 11.0.26 y OpenTelemetry 1.65.0 | 1.0.4 | 3.0.1 | 3.0.1 | 2.0.2 | 1.2.0 | 0.1.1 |
| **4.0.0** | 4.0.8, con Tomcat 11.0.26 y OpenTelemetry 1.65.0 | 3.0.0 | 4.0.0 | 4.0.0 | 3.0.0 | 1.2.0 | 0.1.1 |

Hasta la 1.0.x, los tres starters se publicaban como `nova-api-standard-starter`, `nova-mask-starter` y `nova-observability-starter`. La 2.0.0 del BOM gestiona los nombres de [ADR-039](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/shared/ADR-039-nombres-de-artefacto-derivados-del-repositorio.md), y fija Tomcat en 11.0.26 porque Spring Boot 4.0.8 todavía trae la 11.0.24, con tres CVE altos. La 2.0.1 quiso pasar `nova-spring-boot-starter` a la 1.0.4, que reexporta los starters con los nombres nuevos, pero solo cambió una propiedad que la entrada no usa: la 2.0.1 y la 2.0.2 siguieron gestionando la 1.0.3. La 2.0.2 pasa `nova-observability-spring-boot-starter` a la 2.0.1, porque la 2.0.0 no resuelve: pide `opentelemetry-semconv-incubating` 1.43.0, una versión que no existe. La 2.0.3 gestiona por fin `nova-spring-boot-starter` 1.0.4 e importa `opentelemetry-instrumentation-bom` 2.31.1 antes que Spring Boot. Sin ese import, en Maven el núcleo de OpenTelemetry queda en la 1.55.0 que fija Spring Boot 4.0.8, y el starter de observabilidad, construido con la instrumentación 2.31.1, falla al arrancar con `NoSuchFieldError`. La 2.1.0 suma la familia `nova-secrets` en la 1.0.1, que se explica más abajo, y pasa `nova-observability-spring-boot-starter` a la 2.0.2, construida sobre Spring Boot 4.0.8 como el resto de la plataforma. La 2.2.0 suma la familia `nova-idempotency` en la 0.1.1. La 3.0.0 gestiona el modelo de errores por capas de [ADR-031](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/shared/ADR-031-modulo-de-errores-por-capas-con-trazabilidad.md): `nova-api-standard` 1.1.0 y los dos starters de `nova-java-08-commons-spring-boot-starter` en la 3.0.0. Es mayor porque la 3.0.0 del starter de API cambia lo que un cliente recibe ante un error; la receta está más abajo. La 3.0.1 pasa los dos starters a la 3.0.1, que registra los records del sobre para la imagen nativa: con la 3.0.0, cada respuesta de un servicio nativo terminaba en 500.

La 4.0.0 pone al día lo que el BOM gestiona con las versiones mayores que salieron después de la 3.1.0: `nova-api-standard-spring-boot-starter` y `nova-mask-spring-boot-starter` en la 4.0.0, `nova-observability-spring-boot-starter` en la 3.0.0, `nova-spring-boot-starter` en la 3.0.0 y `nova-api-standard-quarkus-extension` en la 3.0.0. Es mayor porque cuatro de las cinco cambian lo que recibe un servicio que solo sube la versión del BOM (el starter de API solo cambia de número, porque comparte versión con el de enmascaramiento); la receta de cada salto está en [«Migrating to 4.0.0»](#migrating-to-400). Spring Boot 4.0.8, Quarkus 3.33.3.3, Tomcat 11.0.26 y la instrumentación de OpenTelemetry 2.31.1 no cambian, porque son con los que se construyeron esas versiones. Las librerías puras de `nova-bom` ya estaban en lo último publicado: `nova-api-standard` 1.1.0 es la que piden los starters 4.0.0 y la extensión 3.0.0. Además, las cuatro entradas de starters de `nova-spring-boot-bom` usan ahora su propiedad en lugar de un literal, y el CI comprueba que el meta-starter trae cada starter que el BOM gestiona ([«Prueba de completitud»](#prueba-de-completitud-adr-052)).

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
- **Consumidores Gradle** (via `api(platform("pe.edu.nova.java:nova-spring-boot-bom:4.0.0"))`): SÍ ven las 4 librerías gestionadas, porque Gradle lee el modelo POM efectivo completo (incluyendo lo heredado del `<parent>`). Así es como `nova-spring-boot-starter` declara `api("pe.edu.nova.java.libs:nova-date-utils")` sin versión y funciona.
- **Consumidores Maven** que importen `nova-spring-boot-bom` con `<scope>import</scope>` (la forma estándar/correcta de consumir un BOM en Maven) **NO** heredan la gestión de versiones de las 4 librerías puras — Maven's `import` scope solo trae el `<dependencyManagement>` propio del POM importado, no el de sus padres transitivos. Si necesitas una versión gestionada de `nova-date-utils` en un proyecto Maven, importa **también** `nova-bom` explícitamente, o fija la versión manualmente.

**Familia `nova-secrets`.** Desde la 2.1.0, este BOM gestiona la familia `nova-secrets` en la 1.0.1 ([ADR-041](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/java/ADR-041-un-repositorio-por-capacidad.md)): las librerías `nova-secrets`, `nova-secrets-vault` y `nova-secrets-aws-secrets-manager` (`pe.edu.nova.java.libs`) y el starter `nova-secrets-spring-boot-starter` (`pe.edu.nova.java.starters`). `nova-java-23-secrets` publica los cuatro con una sola versión, así que el BOM los gestiona con una sola propiedad, `nova-secrets.version`. A diferencia de las cuatro librerías puras de `nova-bom`, las tres librerías de la familia sí llegan a los consumidores Maven que importan este BOM, porque están en su propio `dependencyManagement`. La 3.1.0 la pasa a la 1.2.0, que suma `nova.secrets.import` ([ADR-049](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/shared/ADR-049-secretos-en-quarkus-y-nestjs.md)), y desde esa versión `nova-quarkus-bom` también la gestiona, con `nova-secrets-quarkus-extension` en lugar del starter. El módulo de deployment de la extensión no se gestiona: Quarkus lo resuelve solo, con la misma versión. Micronaut todavía no tiene conector.

**Familia `nova-idempotency`.** Desde la 2.2.0, este BOM gestiona la familia `nova-idempotency` en la 0.1.1 ([ADR-047](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/shared/ADR-047-idempotencia-detras-de-un-contrato.md)): las librerías `nova-idempotency` y `nova-idempotency-jdbc` (`pe.edu.nova.java.libs`) y el starter `nova-idempotency-spring-boot-starter` (`pe.edu.nova.java.starters`), con una sola propiedad, `nova-idempotency.version`, igual que secretos. Todavía es 0.x: la 1.0.0 llega cuando pedidos de Plaza valide la API. La extensión de Quarkus llega con su primer consumidor.

### `nova-quarkus-bom` (extiende `nova-bom` + Quarkus)

| `nova-quarkus-bom` | Quarkus | `nova-api-standard-quarkus-extension` | familia `nova-secrets` |
|---|---|---|---|
| **2.0.0** | 3.33.3.3 LTS | 2.0.1 | - |
| **2.0.1** | 3.33.3.3 LTS | 2.0.1 | - |
| **2.0.2** | 3.33.3.3 LTS | 2.0.1 | - |
| **2.0.3** | 3.33.3.3 LTS | 2.0.1 | - |
| **2.1.0** | 3.33.3.3 LTS | 2.0.1 | - |
| **2.2.0** | 3.33.3.3 LTS | 2.0.1 | - |
| **3.0.0** | 3.33.3.3 LTS | 2.0.1 | - |
| **3.0.1** | 3.33.3.3 LTS | 2.0.1 | - |
| **3.1.0** | 3.33.3.3 LTS | 2.0.1 | 1.2.0 |
| **4.0.0** | 3.33.3.3 LTS | 3.0.0 | 1.2.0 |

Hasta la 1.0.2, este BOM pedía `nova-quarkus-api-ext:1.0.1`, un paquete que ya no existe en el registro, así que no resolvía. La 4.0.0 pasa `nova-api-standard-quarkus-extension` a la 3.0.0, con los errores por capas de [ADR-050](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/java/ADR-050-errores-por-capas-en-quarkus.md). Las extensiones se gestionan por su módulo de runtime: el de deployment (`-deployment`) no se declara, porque Quarkus lo resuelve desde el descriptor de la extensión (`deployment-artifact`, en `META-INF/quarkus-extension.properties`) con la misma versión que el runtime, así que no puede quedar desalineado. Cuando este BOM gestione la meta-extensión `nova-quarkus-extension` ([ADR-052](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/java/ADR-052-meta-extension-de-quarkus.md)), la prueba de completitud empieza a exigirle cada `*-quarkus-extension` de esta tabla.

### `nova-micronaut-bom`

Importa `micronaut-platform` 5.0.4 y todavía no gestiona ningún artefacto de Nova.

## Migrating to 4.0.0

La 4.0.0 es mayor porque cinco artefactos que el BOM gestiona subieron de versión mayor, y cuatro de esos saltos cambian lo que recibe un servicio que solo sube la versión del BOM. La receta de cada uno vive en el README de su repositorio; esta tabla dice cuál leer.

| Artefacto | BOM 3.1.0 | BOM 4.0.0 | Qué cambia para un servicio | Receta |
|---|---|---|---|---|
| `nova-api-standard-spring-boot-starter` | 3.0.1 | 4.0.0 | Nada: sale en la 4.0.0 porque el repositorio publica sus dos starters con una sola versión. Quien viene de un BOM 2.x cruza además el salto de los errores por capas de ADR-031 | [«Migrating to 3.0.0»](https://github.com/ahincho/nova-java-08-commons-spring-boot-starter#migrating-to-300) y [«Migrating to 4.0.0»](https://github.com/ahincho/nova-java-08-commons-spring-boot-starter#migrating-to-400) de `nova-java-08-commons-spring-boot-starter` |
| `nova-mask-spring-boot-starter` | 3.0.1 | 4.0.0 | Enmascara solo lo que lleva `@Masked`, o está en una clase con `@MaskedClass`. Hasta la 3.0.1 también enmascaraba por el nombre del campo, y el `name` de un producto salía como `T***`. Lo anterior se recupera con `nova.mask.infer-by-field-name: true` | [«Migrating to 4.0.0»](https://github.com/ahincho/nova-java-08-commons-spring-boot-starter#migrating-to-400) de `nova-java-08-commons-spring-boot-starter` |
| `nova-observability-spring-boot-starter` | 2.0.2 | 3.0.0 | Ya no exporta a `http://localhost:4318` por defecto: sin `nova.observability.otlp.endpoint` (o `OTEL_EXPORTER_OTLP_ENDPOINT`) no exporta nada, y `/actuator/health` no reporta un collector que nadie configuró | [«Migrating to 3.0.0»](https://github.com/ahincho/nova-java-09-observability-spring-boot-starter#migrating-to-300) de `nova-java-09-observability-spring-boot-starter` |
| `nova-spring-boot-starter` (meta-starter) | 1.0.4 | 3.0.0 | Trae también observabilidad y secretos, declara la versión de cada starter y ya no importa este BOM (ADR-052): un servicio que lo usa sin el BOM recibe los starters 4.0.0 y 3.0.0, no los 2.x. Cruza la 2.0.0 y la 3.0.0 | [«Migrating to 2.0.0»](https://github.com/ahincho/nova-java-12-spring-boot-starter#migrating-to-200) y [«Migrating to 3.0.0»](https://github.com/ahincho/nova-java-12-spring-boot-starter#migrating-to-300) de `nova-java-12-spring-boot-starter` |
| `nova-api-standard-quarkus-extension` | 2.0.1 | 3.0.0 | El éxito sale en el sobre de Nova y cada error sale por capas (ADR-050). `quarkus.index-dependency` para la extensión ya no hace falta, y con él el build falla | [«Migrating to 3.0.0»](https://github.com/ahincho/nova-java-10-api-standard-quarkus-extension#migrating-to-300) de `nova-java-10-api-standard-quarkus-extension` |

Las demás versiones que el BOM gestiona no cambian: `nova-secrets` 1.2.0, `nova-idempotency` 0.1.1 y las cuatro librerías puras de `nova-bom`.

## Cómo consumir

### Maven

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>pe.edu.nova.java</groupId>
      <artifactId>nova-spring-boot-bom</artifactId>
      <version>4.0.0</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
    <!-- Si tu proyecto usa alguna libreria pura directamente (no solo starters),
         importa tambien el BOM raiz -->
    <dependency>
      <groupId>pe.edu.nova.java</groupId>
      <artifactId>nova-bom</artifactId>
      <version>4.0.0</version>
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
    api(platform("pe.edu.nova.java:nova-spring-boot-bom:4.0.0"))
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

## Prueba de completitud (ADR-052)

El meta-starter `nova-spring-boot-starter` existe para que un servicio declare una sola dependencia y reciba todos los starters de Nova. Se quedó atrás porque nada comprobaba que los trajera todos: la 1.0.4 no traía el starter de observabilidad, y además declaraba los demás sin versión porque importaba el BOM 2.0.0, así que repartía los starters 2.x. El BOM es el único lugar que conoce todos los starters, así que la prueba vive aquí ([ADR-052](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/java/ADR-052-meta-extension-de-quarkus.md), regla 2).

**Qué comprueba.** Cada `*-spring-boot-starter` que `nova-spring-boot-bom` gestiona tiene que estar declarado, con su versión explícita y la misma que gestiona el BOM, en el POM publicado de `nova-spring-boot-starter` (en la versión que el BOM gestiona). Falla si falta un starter, si la versión es otra o si el meta-starter lo declara sin versión. El propio `nova-spring-boot-starter` no se compara contra sí mismo: es la meta-dependencia, no uno de sus miembros.

La misma prueba aplica a `nova-quarkus-bom`: cada `*-quarkus-extension` que gestione tiene que estar en la meta-extensión `nova-quarkus-extension`. Hoy ese BOM no la gestiona, porque el repositorio `nova-java-26-quarkus-extension` todavía no existe; la prueba lo dice en el log y pasa, y empieza a exigir en cuanto el BOM la gestione.

**Qué deja fuera, a propósito.** La lista está en `FAMILIES`, dentro de [`scripts/check_meta_completeness.py`](scripts/check_meta_completeness.py), con la razón de cada entrada. Una exclusión que ya no aplica, porque el BOM dejó de gestionar el starter o porque el meta-starter ya lo trae, también rompe la prueba, para que la lista no se quede vieja.

| Excluido | Razón |
|---|---|
| `nova-idempotency-spring-boot-starter` | [Enmienda de ADR-052](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/java/ADR-052-meta-extension-de-quarkus.md): se enciende sola, exige la tabla de su almacén JDBC y es 0.x. Entra cuando no cambie nada sin configurarla, en una versión 1.x |

**Dónde corre.** En cada pull request (el job `meta-completeness` de `ci.yml`) y antes de publicar el BOM (`publish.yml`, que no publica si la prueba falla). Eso fija el orden de publicación de ADR-052: sale el artefacto, después el meta-starter que lo trae y por último el BOM. Si el BOM saliera antes, el meta-starter que él gestiona no existiría o traería versiones viejas, y la prueba lo frena.

**Cómo correrla.** Lee GitHub Packages, así que necesita un token con `read:packages`:

```bash
GITHUB_TOKEN=$(gh auth token --user ahincho) python3 scripts/check_meta_completeness.py
python3 -m unittest discover -s scripts -v   # las pruebas de la prueba, sin red
```

Termina con 0 si pasa, con 1 si falta algo o hay una versión distinta, y con 2 si no pudo leer lo que tenía que comprobar (sin token, sin red o con el POM sin publicar). Cuando falla, casi siempre falta publicar el meta-starter con la versión nueva: es un PR en `nova-java-12-spring-boot-starter`, con la versión de cada starter escrita en su build (regla 1 de ADR-052), y el BOM sale después. Excluir un starter es una decisión de arquitectura: se agrega a `FAMILIES` con su razón, en el mismo PR que la documenta en el ADR.

## Cómo se mantiene esta matriz

No existe un `gradle/libs.versions.toml` (version catalog) compartido entre los 9 repos Gradle — cada `build.gradle.kts` declara sus propias versiones de forma independiente. Esta tabla es **mantenida manualmente**: actualízala cada vez que se publique una versión nueva de cualquier BOM o de cualquier artefacto que un BOM gestione. Fuente de verdad para "qué está realmente publicado": tags Git (`v*`) + `.release-please-manifest.json` + `CHANGELOG.md` de cada repo — **no** el `gradle.properties`/`pom.xml` del working tree (que normalmente queda en `0.1.0-SNAPSHOT`/`-SNAPSHOT` entre releases). Para un artefacto de Nova, la forma de confirmarlo es `gh api users/ahincho/packages/maven/<groupId>.<artifactId>/versions --jq '.[0].name'`.

Este repositorio no usa release-please: la versión del BOM se sube a mano en el pull request (el `pom.xml` raíz y el `<parent>` de los tres módulos) y se publica con el workflow `Publish BOM`, que se lanza a mano después del merge.

Ver también: [ADR-018 — Política de versionado y bump](https://github.com/ahincho/nova-shared-01-docs/blob/main/adrs/versioning/ADR-018-politica-de-versioning-y-bump.md), [docs/java/06-semantic-versioning-en-java.md](https://github.com/ahincho/nova-shared-01-docs/blob/main/java/06-semantic-versioning-en-java.md) (§11.9.30, NOVA-SEMVER-22).

## License

Eclipse Public License 2.0 — see [LICENSE](LICENSE).

Copyright © 2026 Angel Hincho.
