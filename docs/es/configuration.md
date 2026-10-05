# Configuración

La configuración se proporciona al importar la librería. No necesita un alias.

```robotframework
*** Settings ***
Library    RequestReporter
...    output_dir=${OUTPUT DIR}/cases
...    language=en
...    redact_headers=Authorization,Proxy-Authorization,Cookie,Set-Cookie,X-API-Key
...    redact_body_fields=access_token,refresh_token,client_secret,password,token,api_key
```

| Parámetro | Comportamiento |
|---|---|
| `output_dir` | Por defecto, `${OUTPUT DIR}/cases`. |
| `language` | Solo `en` para la interfaz del reporte; los nombres y labels conservan el idioma del test. |
| `redact_headers` | Nombres separados por comas; no distingue mayúsculas. Reemplaza la lista predeterminada. |
| `redact_body_fields` | Campos JSON/form/query, también anidados. Reemplaza la lista predeterminada. |

## Datos sensibles

Por defecto se ocultan Authorization, Proxy-Authorization, Cookie, Set-Cookie y
X-API-Key, además de los campos del ejemplo. Los valores sensibles conocidos se
ocultan también en mensajes y datos posteriores.

!!! warning "HTML y logs tienen configuraciones independientes"
    La redacción aplica al HTML de esta librería. Los logs de Robot y
    RequestsLibrary pueden contener los argumentos originales. Agrega los nombres
    sensibles específicos de tu API y configura también el logging de tus pruebas.

Responses binarios se resumen con su tamaño. Los bodies multipart no se incrustan.
La librería no mide el total de bytes transferidos por la conexión.

## Tema y copia de headers

El botón Light/Dark sigue inicialmente la preferencia del sistema. Cuando el
navegador permite almacenamiento local, recuerda tu elección. CSS y JavaScript
quedan incluidos en el HTML, sin dependencias de red.

Headers ofrece **Table** y **JSON**. El icono de copia obtiene JSON indentado,
con los valores sensibles ocultos. Si el navegador bloquea el clipboard, muestra
un campo seleccionable con el mismo JSON para copiar manualmente.

## Paralelismo

Configura directorios distintos por worker al usar Pabot. No compartas un
`output_dir` físico entre procesos que escriban al mismo tiempo.
