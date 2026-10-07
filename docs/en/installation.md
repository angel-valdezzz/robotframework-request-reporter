---
tags:
  - Usage
---

# Installation

Use Python 3.12+ and Robot Framework 7.5+ within the 7.x series.

## Install from PyPI

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

RequestsLibrary is installed separately because it executes HTTP. Request Reporter records the evidence from responses you provide.

## Install a wheel

Download a distribution from [PyPI](https://pypi.org/project/robotframework-request-reporter/#files) or the GitHub Actions `distribution` artifact. Replace the example filename with your downloaded wheel.

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

The wheel includes the report template, CSS and JavaScript. MkDocs, Ruff and documentation tools are unnecessary for running your tests.

[Create your first case](usage.md){ .md-button .md-button--primary }

## Work from source

```bash
git clone https://github.com/angel-valdezzz/robotframework-request-reporter.git
cd robotframework-request-reporter
git checkout main
poetry install
poetry build
```

Read the [development workflow](development.md) before contributing changes.
