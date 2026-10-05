# Troubleshooting

??? question "A request is missing"
    RequestsLibrary imports do not intercept every call. Pass each response to `Capture Response`. If a timeout happened first, check **Failures → Execution errors**; no response exists to capture. Use `Capture Request Error` to explicitly document a failed attempt.

??? question "The case fails but every assertion passed"
    Robot can fail outside `Assert`, in setup, teardown or data parsing. Inspect Execution errors and expand Robot's original final message. Not every case failure is a failed assertion.

??? question "JSON parsing failed"
    Capture the response before `${response.json()}` so its body and headers remain available even if parsing fails.

??? question "Headers do not copy automatically"
    Some browsers block clipboard access for local files. A field displays indented JSON for manual selection and copying.

??? question "Two tests have the same name"
    Filenames receive `_2`, `_3`, etc. The title retains Robot's original name. Use unique names for clarity.

??? question "Libdoc cannot find the library"
    Generate it inside the environment where the package is installed:

    ```bash
    poetry run python -m robot.libdoc RequestReporter keywords.html
    ```

??? question "The HTML cannot be written"
    Check output directory permissions and free space. If evidence generation fails, the library marks the case FAIL and records the error in Robot.

[Configuration](configuration.md){ .md-button }
[Keyword reference](keywords/index.html){ .md-button }
