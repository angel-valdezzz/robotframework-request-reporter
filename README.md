# Robot Framework Request Reporter

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-wordmark-dark.svg">
  <img src="docs/assets/logo-wordmark.svg" alt="Request Reporter" width="380">
</picture>

**One standalone HTML evidence report per Robot Framework API test case.**

**English** · [Español](README.es.md)

[User guide](https://angel-valdezzz.github.io/robotframework-request-reporter/) · [Keyword reference](https://angel-valdezzz.github.io/robotframework-request-reporter/keywords/) · [PyPI](https://pypi.org/project/robotframework-request-reporter/) · [Visual examples](https://angel-valdezzz.github.io/robotframework-request-reporter/examples/report.html)

## Features

- Multiple captured HTTP exchanges linked to executed assertions.
- Summary, request overview, failure navigation and searchable bodies.
- Protected headers and JSON/form/query fields.
- Offline HTML with keyboard navigation and light/dark themes.

## Installation

Python 3.12+ and Robot Framework 7.5+. RequestsLibrary executes HTTP and is installed separately.

```bash
pip install robotframework-request-reporter robotframework-requests
```

## Quick start

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

Use an available service URL. The listener is registered automatically and writes reports to `${OUTPUT DIR}/cases`; no separate generation keyword is required. Capture each response before validating or parsing it. `Assert` records and propagates the real assertion result.

## Configuration and limitations

Configure `output_dir`, `redact_headers` and `redact_body_fields` on import. The report UI supports English; business labels may use any language. Documentation language selection does not change generated report controls.

Redaction affects this HTML only; Robot and RequestsLibrary logging remain independent. Binary responses and multipart bodies are summarized. Use `Capture Request Error` for explicit failed HTTP attempts and propagate the original error.

Pabot workers need separate physical output directories. Each HTML contains one case; PDF and a suite-wide dashboard are outside this library. Abrupt termination may prevent finalization. Earlier compatibility keywords were removed in 0.4; use `Capture Response` and `Assert`.

## Examples

The [executable API example](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main) includes a fictitious local API and DataDriver cases. The documentation includes passing and failing HTML examples.

## Development and contribution

```bash
poetry install
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy src
poetry run python scripts/verify.py
poetry run python docs/scripts/build_site.py
poetry build
```

Submit changes through a pull request with passing checks. Update both documentation languages. Libdoc translations live in `docs/translations/es/libdoc.json`; builds reject missing or stale entries.

## License

This repository does not currently include a license file.
