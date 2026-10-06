# Desarrollo y publicación

## Calidad y aceptación

```bash
poetry install
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy src
poetry run python scripts/verify.py
poetry build
poetry run twine check dist/*
poetry run python docs/scripts/build_site.py
```

Las pruebas usan Robot Framework, RequestsLibrary y una API en loopback. Seis casos
fallan intencionalmente para verificar el estado final y sus evidencias. El verificador
comprueba los resultados esperados y devuelve error si aparecen diferencias.

## Libdoc

La biblioteca declara `doc_format="MARKDOWN"`. Robot 7.5 soporta Markdown en los
docstrings y la referencia se obtiene desde la librería instalada:

```bash
poetry run python -m robot.libdoc RequestReporter site/keywords/index.html
```

Markdown y Pygments son dependencias de documentación, no de ejecución. Los ejemplos
usan bloques `robotframework`; `[Assert]` enlaza una keyword en Libdoc. La importación
no crea archivos ni requiere un test activo, para poder generar la referencia.

## Actions

- `ci.yml`: lint, formato, tipos, suites Robot, construcción y verificación del WHL instalado.
- `pages.yml`: MkDocs, Libdoc y reporte generado; publica las tres rutas juntas.
- `release.yml`: construir distribución y publicar en PyPI desde una release.

Pages usa un sitio por repositorio. Se despliega desde `main` después de fusionar un PR con CI exitoso.
Los cambios se desarrollan en ramas `feat/`, `fix/` o `docs/`; `main` requiere
pull request y el check `verify`, sin aprobación externa obligatoria.

## Trusted Publishing

La versión 0.4.0 se publicó mediante Trusted Publishing desde `release.yml`.
Para configurar un publisher equivalente:

| Campo | Valor |
|---|---|
| Project name | robotframework-request-reporter |
| GitHub owner | angel-valdezzz |
| Repository | robotframework-request-reporter |
| Workflow filename | release.yml |
| Environment name | pypi |

El workflow ya utiliza OIDC y `pypa/gh-action-pypi-publish`, sin tokens guardados.
Configurar el pending publisher no reserva el nombre. La publicación se ejecuta al
publicar una release estable cuyo tag, por ejemplo `v0.4.0`, coincida con pyproject.toml.

El publisher inicial se registró sin restricción de environment (`Any`). El workflow
usa el entorno `pypi`; se puede limitar el publisher a ese entorno.
No se requiere compartir una contraseña ni guardar un API token.

## Ejemplo instalado desde PyPI

El repositorio [robotframework-api-testing](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main)
instala la versión publicada, ejecuta una API local ficticia y verifica un caso
individual y dos casos DataDriver. Cada caso genera su propio HTML.

## Cambio de compatibilidad en 0.4

La versión 0.4 retira las keywords de compatibilidad anteriores. Las suites y recursos deben usar Capture Response y Assert. El import público es RequestReporter.

## Documentación bilingüe

El inglés vive en `docs/en/` y se publica en la raíz. El español vive en `docs/es/`
y se publica bajo `/es/`. Conserva los mismos nombres de página en ambos idiomas.
Las traducciones de Libdoc viven en `docs/translations/es/libdoc.json`; la compilación
rechaza entradas faltantes o desactualizadas. El menú nativo de Libdoc cambia sus
controles y las descripciones. Los nombres de keywords y parámetros se conservan.
