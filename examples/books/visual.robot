*** Settings ***
Library           RequestsLibrary
Library           RequestReporter    language=${REPORT_LANGUAGE}
Library           Fixture.py

Suite Setup       Start Fixture
Suite Teardown    Stop API


*** Variables ***
${REPORT_LANGUAGE}    en


*** Test Cases ***
Inspect book catalog
    ${health}=    GET    ${BASE_URL}/health    expected_status=anything    timeout=2
    ${health_id}=    Capture Response    Health check    ${health}
    Assert    ${health_id}    Health status    Should Be Equal As Integers    ${health.status_code}    200
    ${catalog}=    GET    ${BASE_URL}/books    expected_status=anything    timeout=2
    ${catalog_id}=    Capture Response    List books    ${catalog}
    Assert    ${catalog_id}    Catalog status    Should Be Equal As Integers    ${catalog.status_code}    200
    Assert    ${catalog_id}    Catalog has books    Should Not Be Empty    ${catalog.json()}
    ${book}=    GET    url=${BASE_URL}/books/42?api_key=fake-book-SECRET    expected_status=anything    timeout=2
    ${book_id}=    Capture Response    Consult book    ${book}
    Assert    ${book_id}    Book status    Should Be Equal As Integers    ${book.status_code}    200
    ${body}=    Set Variable    ${book.json()}
    Assert    ${book_id}    Book title must contain a value    Should Not Be Empty    ${body}[title]


*** Keywords ***
Start Fixture
    ${url}=    Start API
    VAR    ${BASE_URL}    ${url}    scope=SUITE
