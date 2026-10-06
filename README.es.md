# Robot Framework Request Reporter

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-wordmark-dark.svg">
  <img src="docs/assets/logo-wordmark.svg" alt="Request Reporter" width="380">
</picture>

**Un reporte HTML autocontenido de evidencia por caso de pruebas API en Robot Framework.**

[English](README.md) · **Español**

[Manual de usuario ↗](https://angel-valdezzz.github.io/robotframework-request-reporter/es/) · [Referencia de keywords ↗](https://angel-valdezzz.github.io/robotframework-request-reporter/es/keywords/) · [PyPI ↗](https://pypi.org/project/robotframework-request-reporter/) · [Ejemplos visuales ↗](https://angel-valdezzz.github.io/robotframework-request-reporter/es/examples/report.html)


[![PyPI](https://img.shields.io/pypi/v/robotframework-request-reporter?logo=pypi)](https://pypi.org/project/robotframework-request-reporter/)
![Python](https://img.shields.io/pypi/pyversions/robotframework-request-reporter?logo=python)
![Robot Framework](https://img.shields.io/badge/Robot_Framework-compatible-00A6A6?logo=robotframework)
[![License](https://img.shields.io/github/license/angel-valdezzz/robotframework-request-reporter)](LICENSE)
[![CI](https://github.com/angel-valdezzz/robotframework-request-reporter/actions/workflows/ci.yml/badge.svg)](https://github.com/angel-valdezzz/robotframework-request-reporter/actions/workflows/ci.yml)

## Funcionalidades

- Varios intercambios HTTP capturados y vinculados con assertions ejecutadas.
- Resumen, tabla de requests, navegación de fallos y búsqueda en cuerpos.
- Protección de headers y campos JSON/form/query.
- HTML sin conexión con navegación por teclado y temas claro/oscuro.

## Instalación

Python 3.12+ y Robot Framework 7.5+. RequestsLibrary ejecuta HTTP y se instala por separado.

```bash
pip install robotframework-request-reporter robotframework-requests
```

## Uso rápido

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestReporter

*** Test Cases ***
Health
    ${response}=    GET    http://localhost:8000/health    expected_status=anything
    ${id}=    Capture Response    Health    ${response}
    Assert    ${id}    HTTP status
    ...    Should Be Equal As Integers    ${response.status_code}    200
```

Utiliza la URL de un servicio disponible. El listener se registra automáticamente y escribe en `${OUTPUT DIR}/cases`; no exige una keyword de generación. Captura cada response antes de validarlo o analizarlo. `Assert` registra y propaga el resultado real de la assertion.

## Configuración y limitaciones

Configura `output_dir`, `redact_headers` y `redact_body_fields` al importar. La interfaz del reporte admite inglés; las etiquetas de negocio pueden usar cualquier idioma. Seleccionar el idioma de documentación no cambia los controles del reporte generado.

La protección afecta solo este HTML; los logs de Robot y RequestsLibrary son independientes. Los responses binarios y cuerpos multipart se resumen. Usa `Capture Request Error` para intentos HTTP fallidos explícitos y propaga el error original.

Los workers de Pabot requieren carpetas físicas de salida separadas. Cada HTML contiene un caso; PDF y un dashboard global quedan fuera de esta biblioteca. Una terminación abrupta puede impedir su cierre. Las keywords de compatibilidad anteriores se retiraron en 0.4; utiliza `Capture Response` y `Assert`.

## Ejemplos

El [ejemplo API ejecutable](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main) incluye una API local ficticia y casos DataDriver. La documentación incluye HTML aprobados y fallidos.

## Desarrollo y contribución

```bash
poetry install
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy src
poetry run python scripts/verify.py
poetry run python docs/scripts/build_site.py
poetry build
```

Envía los cambios mediante un pull request con verificaciones aprobadas. Actualiza ambos idiomas. Las traducciones de Libdoc viven en `docs/translations/es/libdoc.json`; la compilación rechaza entradas faltantes o desactualizadas.

## Licencia

Este repositorio todavía no incluye un archivo de licencia.

## Idioma del reporte

Inglés por defecto. Selecciona español al importar; los nombres, payloads y mensajes conservan su contenido.

```robotframework
*** Settings ***
Library    RequestReporter    language=es
```
