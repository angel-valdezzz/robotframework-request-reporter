# Solución de problemas

??? question "No aparece una request"
    Importar RequestsLibrary no intercepta todas sus peticiones. Entrega el response
    a `Capture Response` después de cada petición. Si ocurrió un timeout antes
    de obtenerlo, revisa **Failures → Execution errors**: no habrá response que capturar.

??? question "El caso es FAIL pero todas las assertions aprobaron"
    Robot puede fallar fuera de `Assert`, durante el setup, teardown o interpretación
    de datos. Revisa Execution errors y despliega el mensaje original de Robot.
    No todo fallo del caso es una assertion fallida.

??? question "El JSON no se pudo interpretar"
    Captura la respuesta antes de llamar a `${response.json()}`. Así conserva el
    body y los headers originales aunque luego falle el parsing.

??? question "Headers no se copian automáticamente"
    Algunos navegadores bloquean el clipboard al abrir archivos locales.
    El botón mostrará un campo con JSON indentado para seleccionarlo y copiarlo.

??? question "Dos tests tienen el mismo nombre"
    Los archivos reciben sufijos `_2`, `_3`, etc. El título sigue siendo el nombre
    original de Robot. Para mayor claridad, usa nombres de caso únicos.

??? question "Libdoc no encuentra la librería"
    Genera la referencia dentro del entorno donde instalaste el paquete:

    ```bash
    poetry run python -m robot.libdoc RequestReporter keywords.html
    ```

??? question "El HTML no logra escribirse"
    Comprueba permisos y espacio en la carpeta de salida. Si no puede generar
    la evidencia, la librería marca el caso como FAIL y registra el error en Robot.

[Configuración](configuration.md){ .md-button }
[Referencia de keywords](keywords/index.html){ .md-button }
