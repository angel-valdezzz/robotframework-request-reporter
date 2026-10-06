# Primer caso y varios requests

Guarda este ejemplo como `tests/distributor.robot`. Sustituye la URL ficticia por
la de tu servicio, o utiliza el [ejemplo ejecutable con API local](https://github.com/angel-valdezzz/robotframework-api-testing/tree/main).

```robotframework hl_lines="12-14 22-25"
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

1. Captura antes de verificar el status o interpretar el body. Así una respuesta
   HTTP inesperada conserva su evidencia. Cada captura devuelve un ID del caso.
2. `VAR` y el acceso `${body}[clave]` permiten trabajar con los datos sin
   `Set Variable` ni `Get From Dictionary` para estas operaciones.

```bash
poetry run robot --outputdir results tests/distributor.robot
```

El archivo queda en `results/cases/Consultar_distribuidor.html`.
El título corresponde al nombre del test. Los nombres repetidos reciben sufijos
`_2`, `_3`, etc.; los nombres de archivo se sanitizan y limitan en longitud.

## Asociar varias requests

Si primero obtienes un token y luego consultas un distribuidor, captura cada
response y conserva ambos IDs. Usa el ID correspondiente en cada `Assert`.
No se asume un “último request” para asociar las assertions.

```robotframework hl_lines="6-8 10"
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

Este fragmento requiere `${BASE_URL}`, `${CLIENT_SECRET}` y las imports del primer
bloque. Consulta la [configuración de datos sensibles](configuration.md).

!!! note "Continuación ante fallos"
    `Assert` registra el resultado y propaga el fallo normal de Robot. La etiqueta
    `robot:continue-on-failure` permite ejecutar comprobaciones independientes
    en una keyword de negocio. Evita aplicarla a pasos dependientes, como obtener
    un token requerido para la siguiente petición.

## Keywords propias

`Assert` puede ejecutar assertions BuiltIn o keywords tuyas. Para las igualdades
habituales muestra Expected/Actual; para una keyword personalizada muestra sus
argumentos y error. Las comprobaciones no ejecutadas no se cuentan como SKIP.

[Consultar keywords](keywords/index.html){ .md-button }
[Usar DataDriver](datadriver.md){ .md-button }

## Intentos sin response

El listener genera el HTML incluso si el test falla antes de Capture Response.
Para asociar explícitamente un timeout o error de conexión con su operación, captura
el intento dentro de una keyword de servicio. Esta keyword no ejecuta HTTP ni cambia
el resultado del test: propaga el fallo después de registrar la evidencia.

```robotframework hl_lines="10-11 14-16"
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

Failed HTTP attempts muestra método, URL protegida y mensaje. No fabrica status,
headers ni bodies. Un HTTP 4xx/5xx sí tiene response: usa Capture Response normalmente.
Los errores de ejecución de Robot y el mensaje final se conservan por separado.
Una terminación abrupta del proceso puede impedir que se cierre el reporte.
