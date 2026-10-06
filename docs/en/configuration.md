# Configuration

Configure the library when importing it. No alias is required.

```robotframework hl_lines="4-6"
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

## Report design and institution branding

Reports use the same navigation, compact status labels and light/dark controls. Evidence keeps captures in Steps and messages in Logs, with level filters and search. Request opens the first captured request; Failures links directly to the affected assertion. PDF and Word share a clean metadata table, light milestone bands and evidence frames with a status accent.

Branding is optional and free. It changes presentation, not case metadata or assertion behavior. With no configuration, the original tool name, logo and palette remain.

```json
{
  "name": "Example QA",
  "palette": {
    "primary": "#164e63",
    "accent": "#155e75",
    "primary_dark": "#67e8f9",
    "accent_dark": "#7dd3fc"
  }
}
```

Use `examples/brand.json` as a runnable starting point. Add `"logo": "logo.png"` to use a local PNG, JPEG or WebP image; its path is relative to the JSON file. Logos are embedded, limited to 5 MiB and resized to at most 512 px. No external request is required to view the report. Colors use six-digit hex values. Primary colors must meet 4.5:1 contrast against the selected control text; invalid configuration fails clearly. PASS, FAIL, WARN and HTTP status colors keep their semantic meaning.

```robotframework hl_lines="2 3"
*** Settings ***
Library    RequestsLibrary
Library    RequestReporter    brand_config=${EXECDIR}/examples/brand.json
```
