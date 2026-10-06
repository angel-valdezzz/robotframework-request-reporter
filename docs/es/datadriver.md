# Casos con DataDriver

DataDriver genera tests de Robot a partir de cada fila. El listener crea un HTML
por test generado, con su propio nombre, requests y assertions.

```bash
poetry add robotframework-datadriver
```

## Datos de entrada

Guarda `distributors.csv` junto al archivo `.robot`:

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

Obtendrás `Distribuidor_1042.html` y `Distribuidor_1087.html` dentro de
`results/cases`. Cada uno puede adjuntarse por separado a Jira.

!!! tip "No necesitas pasar el nombre dos veces"
    DataDriver define el nombre del test y la librería lo obtiene de Robot.
    La fila o el identificador como metadata son opcionales.

!!! warning "Ejecución paralela"
    Para Pabot usa una carpeta de reportes distinta por worker. La escritura
    concurrente en una misma carpeta no está soportada.

[Ejemplo completo con API local](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main){ .md-button }
