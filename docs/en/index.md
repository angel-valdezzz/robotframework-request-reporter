---
template: home.html
title: Request Reporter
description: Turn API exchanges and assertions into a portable report.
---

<div id="overview"></div>

## Capture. Validate. Share.

<div class="grid cards" markdown>

- **01 · Capture Response**

    Keep the HTTP exchange alongside its test case.

- **02 · Assert**

    Associate each validation with the corresponding request.

- **03 · HTML**

    Share a standalone report, ready to open offline.

</div>

<section id="report-preview" class="er-real-report" aria-labelledby="report-preview-title" markdown>

<h2 id="report-preview-title">The report, exactly as generated</h2>

This view loads the HTML produced by the project's executable tests. Explore Summary,
Requests and Failures here, or [open the complete report](examples/report.html).

<iframe src="examples/report.html" title="Genuine Request Reporter HTML report in English" loading="lazy"></iframe>

</section>

## Requirements

| Tool | Compatibility |
| --- | --- |
| Python | 3.12+ |
| Robot Framework | 7.5+, within 7.x |
| RequestsLibrary | Executes HTTP; installed separately |
| DataDriver | Optional; generates cases from tabular data |

## How it works

```mermaid
flowchart TD
    A[RequestsLibrary: execute request] --> B[Capture Response: store response]
    B --> C[Assert: record assertions]
    C --> D[Listener: finish case]
    D --> E[Standalone HTML for Jira]
```

Only explicitly captured exchanges are included. Importing the library registers its listener; no CLI listener argument or generation keyword is required.

!!! tip "Metadata is optional"
    Add environment, identifiers or row data for context. The report works without them or an additional title.

## Choose your route

- **First use:** [install](installation.md) and [run a case](usage.md).
- **Tabular data:** [generate DataDriver cases](datadriver.md).
- **Review results:** [read Summary, Failures and Assertions](report.md).
- **Check arguments:** [Libdoc reference](keywords/index.html).
- **Run the complete project:** [executable example](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main), using Poetry and a fictitious local API.

You can also open a [passing report without metadata](examples/passing.html). Each example contains one case; there is no suite-wide dashboard.
