# Leer el reporte

[Explorar el ejemplo en vivo](examples/report.html){ .md-button .md-button--primary }

## Summary

El encabezado usa el nombre y el estado final del caso de Robot. La fecha se
presenta en UTC, con zona horaria explícita. La duración incluye la ejecución del
caso, setup y teardown del test según los eventos de Robot.

Las cuatro tarjetas muestran requests capturadas, assertions ejecutadas,
aprobadas y fallidas. Los metadatos son opcionales. Si hay fallos, un aviso permite
abrir Failures sin llenar el dashboard con mensajes técnicos.

## Requests y Assertions

Elige una request y consulta **Response**, **Request**, **Headers** o **Assertions**.
Cada assertion tiene su label, keyword, estado y detalles. Las igualdades habituales
muestran Expected/Actual; otras keywords incluyen argumentos y mensaje de error.

| Señal | Interpretación |
|---|---|
| PASS / FAIL / SKIP del encabezado | Estado final del caso de Robot |
| PASS / FAIL de una assertion | Resultado de un `Assert` ejecutado |
| HTTP `2xx`, verde | Respuesta HTTP exitosa |
| HTTP `3xx`, ámbar | Redirección |
| HTTP `4xx` / `5xx`, rojo | Error HTTP del cliente o servidor |
| HTTP `1xx`, azul | Respuesta informativa |

!!! example "Un error HTTP puede ser el resultado esperado"
    Si tu test comprueba que un recurso ausente devuelve `404`, el código HTTP
    tendrá su color de error y la assertion puede ser PASS. Un `200` con datos
    incorrectos también puede terminar en FAIL. Son resultados independientes.

Los métodos GET, POST, PUT, PATCH, DELETE, HEAD y OPTIONS tienen colores propios;
no expresan el resultado del caso. Texto e iconos acompañan los colores.

## Failures

La tabla contiene solo assertions fallidas. Cada fila enlaza a la request y la
assertion exacta. Se genera con los datos capturados por `Assert`; no requiere una
keyword nueva ni repetir información en el `.robot`.

**Execution errors** muestra fallos de keywords fuera de `Assert`, como un timeout,
un error al interpretar JSON o un identificador de request desconocido. Se conservan
el nombre de la keyword y el mensaje de Robot. Fallos manejados por TRY/EXCEPT o
keywords de manejo de errores no se presentan como errores de ejecución sin manejar.

El mensaje final original de Robot permanece desplegable. Puede contener fallos
que ocurren fuera de la ejecución de keywords, por ejemplo al resolver una condición.

!!! note "Lo que no se cuenta"
    Un timeout sin response no fabrica una request. Las assertions que no llegaron
    a ejecutarse no se cuentan como SKIP. SKIP del encabezado corresponde al caso.
    Un caso omitido genera su HTML con nombre, estado y motivo. Conserva la evidencia
    capturada antes de la omisión; si no hubo requests, no incluye evidencia HTTP.
    SKIP significa que el caso fue omitido. Un caso que falla tiene estado FAIL.

## Controles accesibles

Puedes navegar con teclado. Las pestañas de una request aceptan flechas izquierda
/derecha, Home y End. Los enlaces de fallos llevan el foco a la assertion. Ambos
modos de color mantienen labels de estado y controles con nombres accesibles.

## Request y Params

El método y la URL están juntos; el icono junto a la URL copia la dirección ya protegida. HTTP status y duración de la respuesta se muestran debajo. **Params** presenta los query parameters de la URL enviada, incluidas claves repetidas y valores vacíos. La copia usa un array JSON para conservar las repeticiones. Los secretos se ocultan antes de mostrar o copiar los datos.

## Summary y navegación

La tabla **Requests overview** muestra nombre, método, código HTTP, tiempo de respuesta y assertions aprobadas/fallidas. Selecciona el nombre para abrir la request en **Requests**. HTTP status no determina el resultado del test.

**Test case information** muestra fecha UTC, duración y resultado. **Test origin** permite consultar la suite y archivo de origen; el reporte continúa conteniendo un solo test. Los metadatos aparecen únicamente cuando existen.

El resultado explica cuántas assertions fallaron y en cuántas requests. Los errores de ejecución y el motivo de SKIP se muestran aparte. Un test sin assertions no se presenta como una validación completa.

## Explorar los bodies

- **Formatted** permite plegar objetos y arrays JSON con el teclado o el mouse.
- **Raw** muestra el texto completo del contenido capturado. Para JSON, es la representación formateada y protegida, no los bytes originales.
- **Search body** busca claves y valores sin modificar los datos; abre los objetos con coincidencias.
- El icono de copia copia el body completo, aunque esté plegado o haya una búsqueda activa. Si el portapapeles no está disponible, aparece un campo para copiar manualmente.
- Body vacío, respuesta no capturada y contenido binario se distinguen explícitamente.

## Filtrar assertions

Usa **All**, **Failed** o **Passed**. Los filtros no cambian los contadores del Summary. Los enlaces desde Failures abren la assertion correspondiente aunque hubiese otro filtro activo.

No se incluye impresión/PDF, gráficas, Results ni logs. Los folios permanecen en el response body y pueden validarse con Assert.

[Ejemplo aprobado sin metadatos](examples/passing.html){ .md-button }

Los bodies de texto/XML completos se pueden plegar en Formatted y desplegar de nuevo. Raw y la copia conservan todo el texto. HTTP requests cuenta responses capturadas e intentos fallidos registrados; estos últimos aparecen con su operación en Failures → Failed HTTP attempts.


[Spanish report / Reporte en español](examples/report.es.html){ target="_blank" rel="noopener noreferrer" }
