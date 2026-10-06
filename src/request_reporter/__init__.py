"""Generate an independent HTML API evidence report for each Robot Framework test.

Import this library alongside RequestsLibrary. Capture each completed HTTP exchange
and associate assertions with its returned identifier using [Assert]. The library
registers its own listener and writes a report when the test finishes.

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestReporter

*** Test Cases ***
Example
    ${response}=    GET    http://localhost:8000/health    expected_status=anything
    ${id}=    Capture Response    Health    ${response}
    Assert    ${id}    HTTP status
    ...    Should Be Equal As Integers    ${response.status_code}    200
```

See [Importing] for configuration. This library does not execute requests or alter
Robot's failure continuation policy. HTTP transport errors without a response appear
in the test's final error message; they do not produce a fabricated exchange.
"""

from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from requests import Response
from robot.api import logger
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn

from .models import Case, Exchange, ExecutionError, RequestError, Validation
from .redaction import Redactor
from .render import write_report

__version__ = "0.7.0"
_HEADERS = "Authorization,Proxy-Authorization,Cookie,Set-Cookie,X-API-Key"
_FIELDS = "access_token,refresh_token,client_secret,password,token,api_key"


@library(scope="GLOBAL", version=__version__, doc_format="MARKDOWN", auto_keywords=False)
class RequestReporter:
    """Generate one self-contained HTML API evidence report per test case.

    Import alongside RequestsLibrary. Capture completed responses and associate
    validations with the returned exchange identifier. The built-in listener
    writes reports when each test finishes, under Robot's output directory.

    ```robotframework
    *** Settings ***
    Library    RequestsLibrary
    Library    RequestReporter

    *** Test Cases ***
    Health
        ${response}=    GET    ${URL}    expected_status=anything
        ${id}=    Capture Response    Health    ${response}
        Assert    ${id}    HTTP status
        ...    Should Be Equal As Integers    ${response.status_code}    200
    ```

    See [Importing] for output and redaction options. This library does not send
    requests or change Robot's failure continuation policy. Redaction applies
    to its HTML reports only, not Robot's or RequestsLibrary's own logs.
    """

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(
        self,
        output_dir: str | None = None,
        language: str = "en",
        redact_headers: str = _HEADERS,
        redact_body_fields: str = _FIELDS,
        brand_config: str | None = None,
    ) -> None:
        """Configure the reporter without creating files during import or Libdoc.

        | Argument | Meaning |
        | --- | --- |
        | output_dir | Report directory; default is Robot's OUTPUT DIR/cases. |
        | language | Interface language. `en` (default) or `es`. |
        | brand_config | Optional local JSON file with institution name, logo and palette. |
        | redact_headers | Comma-separated header names; matched case-insensitively. |
        | redact_body_fields | Comma-separated JSON/form/query field names. |

        ```robotframework
        *** Settings ***
        Library    RequestReporter    output_dir=${OUTPUT DIR}/cases
        ```

        Metadata and validation labels retain the language provided by the caller.
        Redaction applies to this library's HTML only, not Robot/RequestsLibrary logs.
        Binary responses are represented as a byte-count summary. Uploaded files and
        multipart request bodies are summarized instead of embedded.
        """
        if language not in {"en", "es"}:
            raise ValueError("INVALID_LANGUAGE: expected en or es")
        from .branding import load_branding

        load_branding(brand_config)
        self.brand_config = brand_config
        self.language = language
        self.ROBOT_LIBRARY_LISTENER = self
        self.output_dir = output_dir
        self.redact_headers = redact_headers
        self.redact_body_fields = redact_body_fields
        self.case: Case | None = None
        self.redactor = Redactor(redact_headers, redact_body_fields)
        self.started_at = 0.0
        self._checking = 0
        self._failure_keywords: list[Any] = []

    def start_test(self, data: Any, result: Any) -> None:
        self._checking = 0
        self._failure_keywords = []
        self.redactor = Redactor(self.redact_headers, self.redact_body_fields)
        self.case = Case(
            name=data.name,
            source=str(data.source or ""),
            test_id=result.id,
            started=datetime.now(UTC).isoformat(),
            suite=str(BuiltIn().get_variable_value("${SUITE NAME}", "")),
        )
        self.started_at = perf_counter()

    def end_keyword(self, data: Any, result: Any) -> None:
        """Record leaf failures outside Assert without parsing Robot's message."""
        if self.case is None or self._checking or result.status != "FAIL":
            return
        if any(getattr(item, "status", "") == "FAIL" for item in result.body):
            return
        # Keep result references until parents reach their final status. A failed
        # keyword caught by TRY/EXCEPT or an error-handling keyword is not an
        # unhandled execution error, even when a later step fails the same case.
        self._failure_keywords.append(result)

    def end_test(self, data: Any, result: Any) -> None:
        case = self._current()
        case.status = result.status
        if case.status == "FAIL":
            for failed in self._failure_keywords:
                parent = failed.parent
                handled = False
                while parent is not None and parent is not result:
                    if getattr(parent, "status", "") == "PASS":
                        handled = True
                        break
                    parent = parent.parent
                if not handled:
                    case.execution_errors.append(
                        ExecutionError(
                            keyword=self.redactor.text(failed.name),
                            message=self.redactor.text(failed.message or "Keyword failed"),
                        )
                    )
        case.ended = datetime.now(UTC).isoformat()
        case.message = self.redactor.text(result.message or "")
        case.duration_ms = round((perf_counter() - self.started_at) * 1000, 2)
        output = self.output_dir or str(
            Path(BuiltIn().get_variable_value("${OUTPUT DIR}", ".")) / "cases"
        )
        try:
            path = write_report(case, Path(output), self.redactor, self.language, self.brand_config)
            logger.info(f"API case report: {path}")
        except (OSError, ValueError) as error:
            result.status = "FAIL"
            result.message = (
                result.message + f"\nCould not write API case report: {error}"
            ).strip()
            logger.error(result.message)
        finally:
            self.case = None

    def _current(self) -> Case:
        if self.case is None:
            raise RuntimeError("Reporter keywords must run inside an active Robot test case.")
        return self.case

    @keyword("Set Case Metadata")
    def set_case_metadata(self, **metadata: Any) -> None:
        """Add optional metadata to the current case, replacing matching keys.

        Name, status, source and duration are captured automatically. Metadata is
        optional; no case ID or data row is required to generate a report.

        ```robotframework
        Set Case Metadata    case_id=DIST-002    environment=QA    data_row=2
        ```

        Returns nothing. Raises an error outside an active test. Configured sensitive
        field names are redacted. See [Capture Response].
        """
        self._current().metadata.update(self.redactor.clean(metadata))

    @keyword("Capture Response")
    def capture_response(self, name: str, response: Response) -> str:
        """Capture one RequestsLibrary response and return its case-local request ID.

        `response` must be a requests.Response with a prepared request. Captures the
        method, URL, request/response headers and bodies, status code and elapsed time.
        Capture before checking HTTP status so unsuccessful responses remain visible.

        ```robotframework
        ${response}=    GET    ${URL}    expected_status=anything
        ${id}=    Capture Response    Consult distributor    ${response}
        Assert    ${id}    Status
        ...    Should Be Equal As Integers    ${response.status_code}    200
        ```

        Returns `request-1`, `request-2`, etc. IDs are valid only within the current
        case. Raises an error for an invalid response. See [Assert] for assertions.
        """
        case = self._current()
        if not isinstance(response, Response) or response.request is None:
            raise TypeError("response must be a requests.Response with a prepared request.")
        request = response.request
        request_headers = self.redactor.headers(request.headers)
        response_headers = self.redactor.headers(response.headers)
        request_type = request.headers.get("Content-Type", "")
        if "multipart/" in request_type:
            request_body: Any = "[Multipart body omitted]"
        else:
            request_body = self.redactor.body(request.body, request_type)
        response_type = response.headers.get("Content-Type", "").lower()
        if any(x in response_type for x in ("json", "text/", "xml", "javascript")):
            response_body = self.redactor.body(response.text, response_type)
        else:
            response_body = f"[Binary response: {len(response.content)} bytes]"
        request_id = f"request-{len(case.exchanges) + 1}"
        case.exchanges.append(
            Exchange(
                id=request_id,
                name=name,
                method=request.method or "",
                url=self.redactor.url(request.url or ""),
                status_code=response.status_code,
                duration_ms=round(response.elapsed.total_seconds() * 1000, 2),
                request_headers=request_headers,
                response_headers=response_headers,
                request_body=request_body,
                response_body=response_body,
            )
        )
        return request_id

    @keyword("Capture Request Error")
    def capture_request_error(self, name: str, method: str, url: str, message: str) -> None:
        """Record an HTTP attempt without a response; does not execute HTTP or fail a test.

        Use inside TRY/EXCEPT around the HTTP call, then propagate the original failure.
        Captures only caller-supplied information; never invents status, headers or body.
        URL and message are protected by the reporter's redaction rules.

        ```robotframework
        TRY
            ${response}=    GET    ${URL}    timeout=10    expected_status=anything
        EXCEPT    AS    ${error}
            Capture Request Error    Health    GET    ${URL}    ${error}
            Fail    ${error}
        END
        ```

        Returns nothing. Failed attempts appear in Summary and Failures, separately
        from completed exchanges. Do not use this for HTTP 4xx/5xx responses: capture
        those normally with Capture Response. The actual test status comes from Robot.
        """
        case = self._current()
        protected_url = self.redactor.url(url)
        case.request_errors.append(
            RequestError(
                name=self.redactor.text(name),
                method=method.upper(),
                url=protected_url,
                message=self.redactor.text(message),
            )
        )

    @keyword("Assert")
    def assert_that(self, request_id: str, label: str, assertion_keyword: str, *args: Any) -> Any:
        """Run an assertion keyword, record its result, and propagate normal failures.

        Associates the validation with `request_id`, not an implicit last request.
        Supports Robot BuiltIn assertions and your own user keywords. Positional
        arguments after `assertion_keyword` are forwarded unchanged.

        ```robotframework
        Assert    ${id}    Distributor type
        ...    Should Be Equal As Strings    ${body}[tipoDistribuidor]    AGENTE
        ```

        Returns the assertion's return value on success. Re-raises its failure on
        error, preserving Robot's FAIL status. Use `robot:continue-on-failure` on a
        business validation group when independent checks should all run.

        Standard equality assertions show Expected/Actual. Non-empty checks show
        `non-empty value`; other custom keywords show arguments and the error message.
        Unexecuted checks are not counted. Unknown request IDs fail before execution.
        """
        case = self._current()
        exchange = next((x for x in case.exchanges if x.id == request_id), None)
        if exchange is None:
            raise ValueError(f"Unknown request ID in current case: {request_id}")
        normalized = assertion_keyword.rsplit(".", 1)[-1].replace(" ", "").replace("_", "").lower()
        actual = args[0] if args else None
        expected = None
        if normalized.startswith("shouldbeequal") and len(args) > 1:
            expected = args[1]
        elif normalized == "shouldnotbeempty":
            expected = "non-empty value"
        validation = Validation(
            label=label,
            keyword=assertion_keyword,
            status="PASS",
            actual=self.redactor.clean(actual),
            expected=self.redactor.clean(expected),
            arguments=self.redactor.clean(args),
        )
        exchange.validations.append(validation)
        self._checking += 1
        try:
            return BuiltIn().run_keyword(assertion_keyword, *args)
        except Exception as error:
            validation.status = "FAIL"
            validation.error = self.redactor.text(str(error))
            raise
        finally:
            self._checking -= 1
