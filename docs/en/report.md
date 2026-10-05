# Reading the report

[Explore the live example](examples/report.html){ .md-button .md-button--primary }

## Summary

The header uses the Robot test name and final status. Dates are displayed in UTC with an explicit time zone. Duration includes test execution, setup and teardown according to Robot events.

Four cards show captured requests, executed assertions, passed assertions and failed assertions. Metadata is optional. A failure notice opens Failures without filling the dashboard with technical messages.

## Requests and Assertions

Select a request and inspect **Response**, **Request**, **Headers** or **Assertions**. Each assertion includes its label, keyword, status and details. Common equality checks show Expected/Actual; other keywords show arguments and error messages.

| Signal | Meaning |
| --- | --- |
| Header PASS / FAIL / SKIP | Final Robot test status |
| Assertion PASS / FAIL | Result of an executed `Assert` |
| Green HTTP `2xx` | Successful HTTP response |
| Amber HTTP `3xx` | Redirect |
| Red HTTP `4xx` / `5xx` | Client or server HTTP error |
| Blue HTTP `1xx` | Informational response |

!!! example "An HTTP error can be expected"
    A test checking a missing resource can receive `404` while its assertion passes. A `200` with incorrect data can fail. These are independent results.

GET, POST, PUT, PATCH, DELETE, HEAD and OPTIONS have their own colors, unrelated to test status. Text and icons accompany color.

## Failures

The table contains failed assertions only. Each row links to its exact request and assertion. It uses the data recorded by `Assert`, without extra keywords or duplicated test information.

**Execution errors** shows keyword failures outside `Assert`, such as timeouts, JSON parsing failures or unknown request IDs. Robot's keyword name and message are preserved. Errors handled by TRY/EXCEPT or error-handling keywords are excluded from unhandled execution errors.

Robot's original final message remains expandable and can contain failures outside keyword execution, such as condition evaluation errors.

!!! note "What is not counted"
    A timeout without a response does not fabricate a response. Unexecuted assertions are not counted as SKIP. Header SKIP belongs to the test. A skipped case gets an HTML with its name, status and reason, preserving evidence recorded before the skip. A case with no captured requests has no HTTP evidence. SKIP means omitted; a failed case has FAIL status.

## Accessible controls

Navigate with the keyboard. Request tabs support Left/Right, Home and End. Failure links focus the assertion. Both themes retain status labels and accessible control names.

## Request and Params

Method and URL appear together. The URL icon copies the protected address. HTTP status and response duration appear below. **Params** shows sent query parameters, including repeated keys and empty values. Copying uses a JSON array to preserve repetitions. Secrets are hidden before display or copying.

## Summary navigation

**Requests overview** shows name, method, HTTP code, response time and passed/failed assertions. Select a name to open it in **Requests**. HTTP status does not determine test status.

**Test case information** shows UTC date, duration and result. **Test origin** shows suite and source file; each report still contains one test. Metadata appears only when present.

The result explains how many assertions failed and across how many requests. Execution errors and SKIP reasons are separate. A test without assertions is not presented as fully validated.

## Explore bodies

- **Formatted** allows collapsing JSON objects and arrays by keyboard or mouse.
- **Raw** shows complete captured text. For JSON this is the formatted, protected representation, not original bytes.
- **Search body** searches keys and values without changing data and opens matching objects.
- Copying includes the complete body regardless of collapsed sections or active search. A selectable field provides a fallback when clipboard access is unavailable.
- Empty bodies, uncaptured responses and binary content are distinguished explicitly.

## Filter assertions

Use **All**, **Failed** or **Passed**. Filters do not change Summary counters. Failure links reveal the corresponding assertion even when another filter is active.

There is no print/PDF, charts, Results or logs section. Business identifiers remain in response bodies and can be checked with Assert.

[Passing example without metadata](examples/passing.html){ .md-button }

Complete text/XML bodies can be collapsed and expanded in Formatted. Raw and copying preserve all text. HTTP requests counts captured responses and explicitly recorded failed attempts; those attempts appear with their operation under Failures → Failed HTTP attempts.
