# Configuration

Configure the library when importing it. No alias is required.

```robotframework
*** Settings ***
Library    RequestReporter
...    output_dir=${OUTPUT DIR}/cases
...    language=en
...    redact_headers=Authorization,Proxy-Authorization,Cookie,Set-Cookie,X-API-Key
...    redact_body_fields=access_token,refresh_token,client_secret,password,token,api_key
```

| Parameter | Behavior |
| --- | --- |
| `output_dir` | Defaults to `${OUTPUT DIR}/cases`. |
| `language` | `en` (default) and `es` are supported for the report UI; test names and labels retain their language. |
| `redact_headers` | Comma-separated, case-insensitive names. Replaces the default list. |
| `redact_body_fields` | JSON/form/query fields, including nested fields. Replaces the default list. |

## Sensitive data

Authorization, Proxy-Authorization, Cookie, Set-Cookie, X-API-Key and the fields shown above are hidden by default. Known sensitive values are also hidden in later messages and data.

!!! warning "HTML and logs have independent settings"
    Redaction applies to this library's HTML. Robot and RequestsLibrary logs can contain the original arguments. Add your API's specific sensitive fields and configure test logging as well.

Binary responses are summarized by size. Multipart bodies are not embedded. The library does not measure all bytes transferred over the connection.

## Theme and header copying

Light/Dark initially follows the system preference and remembers your choice when browser storage is available. CSS and JavaScript are embedded in the HTML without network dependencies.

Headers offers **Table** and **JSON**. Copy produces indented JSON with sensitive values hidden. If clipboard access is blocked, a selectable field provides the same JSON for manual copying.

## Parallel execution

Use a distinct report directory per Pabot worker. Do not share one physical `output_dir` between concurrent writers.
