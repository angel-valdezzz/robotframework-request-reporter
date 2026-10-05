# First case and multiple requests

Save this as `tests/distributor.robot`. Replace the fictitious URL with your service, or use the [executable local API example](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main).

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestReporter

*** Variables ***
${BASE_URL}    https://api.qa.example.test

*** Test Cases ***
Consultar distribuidor
    Set Case Metadata    case_id=DIST-001    environment=QA
    ${response}=    GET    ${BASE_URL}/distribuidores/1042    expected_status=anything
    ${id}=    Capture Response    Consultar distribuidor    ${response}    # (1)!
    Assert    ${id}    Código HTTP
    ...    Should Be Equal As Integers    ${response.status_code}    200
    VAR    ${body}    ${response.json()}    # (2)!
    Verificar datos del distribuidor    ${id}    ${body}

*** Keywords ***
Verificar datos del distribuidor
    [Arguments]    ${id}    ${body}
    [Tags]    robot:continue-on-failure
    Assert    ${id}    Tipo de distribuidor
    ...    Should Be Equal As Strings    ${body}[tipoDistribuidor]    AGENTE
    Assert    ${id}    RFC con contenido
    ...    Should Not Be Empty    ${body}[rfc]
```

1. Capture before checking HTTP status or parsing the body, so unexpected responses retain evidence. Each capture returns a case-local ID.
2. `VAR` and `${body}[key]` access allow working with data without `Set Variable` or `Get From Dictionary` for these operations.

```bash
poetry run robot --outputdir results tests/distributor.robot
```

The output is `results/cases/Consultar_distribuidor.html`. Its title is the test name. Repeated names receive `_2`, `_3`, etc.; filenames are sanitized and length-limited.

## Associate multiple requests

If you obtain a token and then query a distributor, capture each response and retain both IDs. Provide the corresponding ID to each `Assert`. There is no implicit “last request”.

```robotframework
*** Keywords ***
Obtener token
    VAR    &{form}    grant_type=client_credentials    client_secret=${CLIENT_SECRET}
    ${response}=    POST    ${BASE_URL}/oauth/token
    ...    data=${form}    expected_status=anything
    ${id}=    Capture Response    Obtener token    ${response}
    Assert    ${id}    Código HTTP
    ...    Should Be Equal As Integers    ${response.status_code}    200
    VAR    ${body}    ${response.json()}
    Assert    ${id}    Token presente    Should Not Be Empty    ${body}[access_token]
    RETURN    ${body}[access_token]
```

This snippet requires `${BASE_URL}`, `${CLIENT_SECRET}` and the first example's imports. See [sensitive data configuration](configuration.md).

!!! note "Continue on failure"
    `Assert` records the result and propagates Robot's normal failure. `robot:continue-on-failure` allows independent checks in a business keyword. Avoid it for dependent steps such as obtaining a required token.

## Custom keywords

`Assert` runs BuiltIn assertions or your own keywords. Common equality checks show Expected/Actual; custom keywords show arguments and errors. Unexecuted checks are not counted as SKIP.

[Keyword reference](keywords/index.html){ .md-button }
[Use DataDriver](datadriver.md){ .md-button }

## Attempts without a response

The listener generates HTML even if the test fails before Capture Response. To explicitly associate a timeout or connection error with its operation, record the attempt in a service keyword. This does not execute HTTP or change test status: propagate the original failure after recording evidence.

```robotframework
*** Settings ***
Library    RequestsLibrary
Library    RequestReporter

*** Test Cases ***
Consultar servicio
    VAR    ${url}    http://localhost:8000/health
    TRY
        ${response}=    GET    ${url}    timeout=10    expected_status=anything
    EXCEPT    AS    ${error}
        Capture Request Error    Health    GET    ${url}    ${error}
        Fail    ${error}
    END
    ${id}=    Capture Response    Health    ${response}
    Assert    ${id}    HTTP status
    ...    Should Be Equal As Integers    ${response.status_code}    200
```

Failed HTTP attempts shows method, protected URL and message, without inventing status, headers or bodies. HTTP 4xx/5xx has a response: use Capture Response normally. Robot execution errors and its final message remain separate. Abrupt process termination may prevent report finalization.
