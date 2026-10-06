# Development and publishing

## Quality and acceptance

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

Tests use Robot Framework, RequestsLibrary and a loopback API. Six cases fail intentionally to verify their final status and evidence. The verifier checks expected results and fails on differences.

## Libdoc

The library declares `doc_format="MARKDOWN"`. Robot 7.5 supports Markdown docstrings. You can generate the original reference directly:

```bash
poetry run python -m robot.libdoc RequestReporter site/keywords/index.html
```

Markdown and Pygments are documentation dependencies, not runtime requirements. Examples use `robotframework` fences; `[Assert]` links a keyword in Libdoc. Importing creates no files and requires no active test.

For the complete bilingual site, run `poetry run python docs/scripts/build_site.py`. English sources live in `docs/en/`, Spanish in `docs/es/`, and shared assets in `docs/assets/`. English is published at the root, Spanish under `/es/`. Keep counterpart filenames identical so the language selector retains the current page.

Libdoc translations live in `docs/translations/es/libdoc.json`. Update the Spanish text and its source SHA-256 when changing a docstring. The build rejects missing, extra or outdated entries. Keyword names, arguments, types and defaults remain unchanged. The native Libdoc language menu switches both controls and keyword descriptions.

## Actions

- `ci.yml`: lint, formatting, types, Robot suites, distribution build and installed wheel verification.
- `pages.yml`: bilingual MkDocs, Libdoc and generated report, published together.
- `release.yml`: distribution build and PyPI publication from a release.

Pages deploys from `main` after a PR with successful CI. Work on `feat/`, `fix/` or `docs/` branches; `main` requires a pull request and the `verify` check, without mandatory external approval.

## Trusted Publishing

Version 0.4.0 was published through Trusted Publishing from `release.yml`.

| Field | Value |
| --- | --- |
| Project name | robotframework-request-reporter |
| GitHub owner | angel-valdezzz |
| Repository | robotframework-request-reporter |
| Workflow filename | release.yml |
| Environment name | pypi |

The workflow uses OIDC and `pypa/gh-action-pypi-publish`, without stored tokens. A pending publisher does not reserve the name. Publishing a stable release triggers publication when its tag matches `pyproject.toml`, for example `v0.4.0` for that version.

The initial publisher had no environment restriction (`Any`). The workflow uses `pypi`; the publisher can be restricted to that environment. No shared password or stored API token is needed.

## Example installed from PyPI

[robotframework-api-testing](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main) installs the published package, runs a fictitious local API and verifies an individual case and two DataDriver cases. Each produces its own HTML.

## Compatibility change in 0.4

Version 0.4 removed the earlier compatibility keywords. Suites and resources use Capture Response and Assert. The public import is RequestReporter.
