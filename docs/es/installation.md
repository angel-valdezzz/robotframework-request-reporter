---
tags:
  - Uso
---

# Instalación

Necesitas Python 3.12+ y Robot Framework 7.5+ dentro de la rama 7.x.

## Instalar desde PyPI

=== "Poetry"

    ```bash
    poetry add robotframework-request-reporter robotframework-requests
    poetry run robot --version
    ```

=== "pip"

    ```bash
    python -m pip install robotframework-request-reporter robotframework-requests
    python -m robot --version
    ```

RequestsLibrary se instala por separado porque es quien ejecuta HTTP. La librería
reportera registra la evidencia de los responses que le entregas.

## Instalar un WHL

Descarga la distribución desde [PyPI](https://pypi.org/project/robotframework-request-reporter/#files)
o desde el artefacto `distribution` de GitHub Actions.

=== "Poetry"

    ```bash
    poetry add ./robotframework_request_reporter-0.4.0-py3-none-any.whl
    poetry add robotframework-requests
    ```

=== "pip"

    ```bash
    python -m pip install ./robotframework_request_reporter-0.4.0-py3-none-any.whl
    python -m pip install robotframework-requests
    ```

El WHL incluye la plantilla, CSS y JavaScript del reporte. MkDocs, Ruff y las
herramientas de documentación no son necesarias para ejecutar tus pruebas.

[Crear el primer caso](usage.md){ .md-button .md-button--primary }

## Trabajar desde el código fuente

```bash
git clone https://github.com/angel-valdezzz/robotframework-request-reporter.git
cd robotframework-request-reporter
git checkout main
poetry install
poetry build
```

Consulta el [flujo de desarrollo](development.md) antes de incorporar cambios.
