Endpoints disponibles para la gestión de herramientas
1. Agregar una herramienta
Endpoint: POST http://127.0.0.1:8000/addTool/

Descripción: Crea una nueva herramienta, proporcionando su nombre y una imagen.

Parámetros (Body):

name (string): Nombre de la herramienta.

image (file): Imagen asociada a la herramienta (formatos permitidos: JPEG, PNG, GIF, WEBP).

Respuesta exitosa:

Código de estado: 201 Created

Cuerpo de la respuesta:


Editar
{
  "message": "Herramienta creada con éxito"
}
Respuestas de error:

400 Bad Request si falta el nombre o la imagen, o si la imagen tiene un formato no válido.

404 Not Found si falta la imagen.

500 Internal Server Error si ocurre un error inesperado.

2. Actualizar una herramienta
Endpoint: PATCH http://127.0.0.1:8000/updateTool/

Descripción: Actualiza los detalles de una herramienta existente.

Parámetros (Body):

id (integer): ID de la herramienta que se desea actualizar.

name (string, opcional): Nuevo nombre de la herramienta.

image (file, opcional): Nueva imagen asociada a la herramienta.

state (integer, opcional): Nuevo estado de la herramienta. (1: Activo, 2: En proceso, 3: Inactivo)

Respuesta exitosa:

Código de estado: 200 OK

Cuerpo de la respuesta:

json

{
  "message": "Herramienta actualizada exitosamente"
}
Respuestas de error:

500 Internal Server Error si ocurre un error inesperado.

3. Obtener todas las herramientas
Endpoint: GET http://127.0.0.1:8000/geTools/

Descripción: Recupera todas las herramientas registradas en el sistema.

Respuesta exitosa:

Código de estado: 200 OK

Cuerpo de la respuesta:

json

[
  {
    "id": 1,
    "name": "Taladro",
    "image": "url_imagen",
    "code": "TA-1",
    "state": 1
  },
  ...
]
Respuestas de error:

500 Internal Server Error si ocurre un error inesperado.

4. Obtener herramienta por ID
Endpoint: GET http://127.0.0.1:8000/getToolById/{tool_id}/

Descripción: Recupera una herramienta específica por su ID.

Parámetros (URL):

tool_id (integer): ID de la herramienta.

Respuesta exitosa:

Código de estado: 200 OK

Cuerpo de la respuesta:

json

{
  "id": 1,
  "name": "Taladro",
  "image": "url_imagen",
  "code": "TA-1",
  "state": 1
}
Respuestas de error:

500 Internal Server Error si ocurre un error inesperado.

5. Eliminar una herramienta
Endpoint: DELETE http://127.0.0.1:8000/deleteTool/{tool_id}/

Descripción: Elimina una herramienta específica por su ID.

Parámetros (URL):

tool_id (integer): ID de la herramienta a eliminar.

Respuesta exitosa:

Código de estado: 200 OK

Cuerpo de la respuesta:

json

{
  "message": "Herramienta eliminada con éxito"
}
Respuestas de error:

500 Internal Server Error si ocurre un error inesperado.

