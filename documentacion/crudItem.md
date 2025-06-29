API de Ítems
Base URL: http://127.0.0.1:8000/item/



🔹 1. Crear Ítem
Método: POST

URL: /additem/

Body:

json

{
  "description": "panel de hierro",
  "units": "metros",
  "amount": 3,
  "unit_value": 50000
}
Respuestas:

✅ 201 Created

json

{ "message": "Item creado exitosamente" }
❌ 400 Bad Request

json

{ "error": "All fields are required" }


🔹 2. Actualizar Ítem
Método: PUT

URL: /updateitem/<int:item_id>



Body (puedes enviar solo los campos a actualizar):

json

{
  "description": "Servicio técnico actualizado",
  "units": "horas",
  "amount": 2,
  "unit_value": 45000
}
Respuestas:

✅ 200 OK

json

{ "message": "Item actualizado exitosamente" }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }

🔹 3. Eliminar Ítem
Método: DELETE

URL: /delete/<int:item_id>

Respuestas:

✅ 204 No Content

json

{ "message": "Item eliminado exitosamente" }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }

🔹 4. Obtener Todos los Ítems
Método: GET

URL: /getitems/

Respuestas:

✅ 200 OK


[
  {
    "id": 1,
    "description": "Instalación eléctrica",
    "units": "metros",
    "amount": 100,
    "unit_value": 1200
  },
  ...
]
🔹 5. Obtener Ítem por ID
Método: GET

URL: /getitem/<int:item_id>

Respuestas:

✅ 200 OK


{
  "id": 1,
  "description": "Instalación eléctrica",
  "units": "metros",
  "amount": 100,
  "unit_value": 1200
}
❌ 404 Not Found


{ "error": "Item not found" }