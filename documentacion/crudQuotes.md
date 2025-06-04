API de Cotizaciones (Quotes)
Base URL: http://127.0.0.1:8000/quote/


🔹 1. Crear Cotización
Método: POST

URL: /addquote/


Body:

json

{
  "description": "Cotización para proyecto de energía",
  "customer_id": 1,
  "options": [2, 4], "id de las opciones"
  "tasks": [
    "Visita técnica",
    "Montaje de paneles",
    "Pruebas de funcionamiento"
  ]
}
Respuestas:

✅ 201 Created


{ "message": "Cotizacion creada exitosamente" }
❌ 400 Bad Request


{ "error": "All fields are required" }
❌ 500 Internal Server Error


{ "error": "Mensaje del error" }


🔹 2. Actualizar Cotización
Método: PUT

URL: /updatequote/<int:quote_id>



Body (solo lo que vas a editar):

json

{
  "description": "Cotización actualizada",
  "customer_id": 2,
  "options": [1],
  "tasks": [
    "Visita técnica",
    "Ajuste de cableado"
  ]
}
Respuestas:

✅ 200 OK

json

{ "message": "Cotizacion actualizada exitosamente" }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }
🔹 3. Eliminar Cotización
Método: DELETE

URL: /delete/<int:quote_id>

Respuestas:

✅ 204 No Content

json


{ "message": "Cotizacion eliminada exitosamente" }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }


🔹 4. Obtener Todas las Cotizaciones
Método: GET

URL: /getquotes/

Respuestas:

✅ 200 OK

json

[
    {
        "id": 1,
        "customer": {
            "id": 1,
            "name": "serenity sas",
            "email": "serenity@gmail.com",
            "phone": "123456"
        },
        "options": [
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
        ],
        "code": "2025-1",
        "description": "oliwis",
        "issue_date": "2025-06-04",
        "state": 1,
        "tasks": [
            "hacer aseo",
            "juen es puta"
        ]
    }
]
🔹 5. Obtener Cotización por ID
Método: GET

URL: /getquote/<int:quote_id>

Respuestas:

✅ 200 OK

json

{
    "id": 1,
    "customer": {
        "id": 1,
        "name": "serenity sas",
        "email": "serenity@gmail.com",
        "phone": "123456"
    },
    "options": [
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
    ],
    "code": "2025-1",
    "description": "oliwis",
    "issue_date": "2025-06-04",
    "state": 1,
    "tasks": [
        "hacer aseo",
        "juen es puta"
    ]
}
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }