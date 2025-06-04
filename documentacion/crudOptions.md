API de Opciones
Base URL: http://127.0.0.1:8000/option/



🔹 1. Crear Opción
Método: POST

URL: /addoption/



Body:

json

{
  "description": "Combo de servicios eléctricos",
  "items": [1, 2, 3] "ID de los items"
}
Respuestas:

✅ 201 Created

json

{ "message": "Option creada exitosamente" }
❌ 400 Bad Request

json

{ "error": "All fields are required" }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }
🔹 2. Actualizar Opción
Método: PUT

URL: /updateoption/<int:option_id>



Body (parcial o completo):

json

{
  "description": "Combo actualizado",
  "items": [2, 3]
}
Respuestas:

✅ 200 OK

json

{ "message": "Option actualizada exitosamente" }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }

🔹 3. Eliminar Opción
Método: DELETE

URL: /delete/<int:option_id>

Respuestas:

✅ 204 No Content

json

{ "message": "Option eliminada exitosamente" }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }
🔹 4. Listar Todas las Opciones
Método: GET

URL: /getoptions/

Respuestas:

✅ 200 OK

json
Copiar
Editar
[
    {
        "id": 1,
        "items": [
            {
                "id": 1,
                "description": "logica",
                "units": "cm2",
                "amount": 3,
                "unit_value": "130000.00",
                "total_value": "390000.00"
            }
        ],
        "name": "pruebis",
        "total_value": "390000.00"
    }
]
🔹 5. Obtener Opción por ID
Método: GET

URL: /getoption/<int:option_id>

Respuestas:

✅ 200 OK

json
Copiar
Editar
{
    "id": 1,
    "items": [
        {
            "id": 1,
            "description": "logica",
            "units": "cm2",
            "amount": 3,
            "unit_value": "130000.00",
            "total_value": "390000.00"
        }
    ],
    "name": "pruebis",
    "total_value": "390000.00"
}
❌ 500 Internal Server Error


{ "error": "Mensaje del error" }