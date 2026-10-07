---
tags:
  - Integration
---

# DataDriver cases

DataDriver generates Robot tests from each row. The listener creates one HTML per generated test, with its own name, requests and assertions.

```bash
poetry add robotframework-datadriver
```

## Input data

Save `distributors.csv` beside the `.robot` file:

```csv
*** Test Cases ***,${number},${expected_type}
Distribuidor 1042,1042,AGENTE
Distribuidor 1087,1087,AGENTE
```

## Suite

```robotframework hl_lines="4-5 18-20 22-23"
*** Settings ***
Library          RequestsLibrary
Library          RequestReporter
Library          DataDriver    file=distributors.csv    dialect=excel
Test Template    Verificar distribuidor

*** Variables ***
${BASE_URL}    https://api.qa.example.test

*** Test Cases ***
Distribuidor ${number}    ${number}    ${expected_type}

*** Keywords ***
Verificar distribuidor
    [Arguments]    ${number}    ${expected_type}
    ${response}=    GET    ${BASE_URL}/distribuidores/${number}
    ...    expected_status=anything
    ${id}=    Capture Response    Consultar distribuidor    ${response}
    Assert    ${id}    Código HTTP
    ...    Should Be Equal As Integers    ${response.status_code}    200
    VAR    ${body}    ${response.json()}
    Assert    ${id}    Tipo de distribuidor
    ...    Should Be Equal As Strings    ${body}[tipoDistribuidor]    ${expected_type}
```

```bash
poetry run robot --outputdir results tests/distributors.robot
```

The output contains `Distribuidor_1042.html` and `Distribuidor_1087.html` in `results/cases`. Each can be attached separately to Jira. The Spanish business names in this example remain valid in an English guide.

!!! tip "No need to provide the name twice"
    DataDriver defines the test name and the library obtains it from Robot. Row data or an identifier in metadata are optional.

!!! warning "Parallel execution"
    Use a separate report directory per Pabot worker. Concurrent writing into one directory is unsupported.

[Complete example with a local API](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main){ .md-button }
