POST http://127.0.0.1:8000/ticket/addticket/
Crea un nuevo ticket de solicitud de herramientas.

Body (JSON):
json

{
  "tools": [1, 2, 3],          // IDs de las herramientas
  "description": "Descripción del problema o solicitud",
  "email": "usuario@example.com",  // Correo del solicitante
  "place": "Lugar donde se necesita el soporte"
}
📤 Respuestas:
200 OK

json

{
  "message": "Ticket creado con exito"
}
400 Bad Request

json

{
  "error": "Faltan datos"
}
500 Internal Server Error

json

{
  "error": "Mensaje de error interno"
}
También se envía una notificación por correo al primer usuario con rol 1 (encargado del ticket).

GET http://127.0.0.1:8000/ticket/tickets/
Obtiene todos los tickets registrados.

📤 Respuestas:
200 OK

json

[
    {
        "id": 1,
        "tools": [
            {
                "id": 1,
                "name": "Taladro",
                "code": "T-1",
                "state": 1,
                "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1743805307/afhimages/mnm6yun2cqcrp3a8rotl.jpg",
                "marca": "makita"
            },
            {
                "id": 2,
                "name": "Rodillo",
                "code": "R-1",
                "state": 1,
                "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1743805322/afhimages/wvo3gcuivn6mgffy1vef.jpg",
                "marca": "makita"
            }
        ],
        "receiver": {
            "id": 1,
            "user": {
                "username": "sebastianscarpetta19@gmail.com",
                "first_name": "sebastian",
                "last_name": "hernandez",
                "email": "sebastianscarpetta19@gmail.com"
            },
            "role": 1
        },
        "applicant": {
            "id": 2,
            "user": {
                "username": "sebastianscarpetta@gmail.com",
                "first_name": "sebastian",
                "last_name": "hernandez",
                "email": "sebastianscarpetta@gmail.com"
            },
            "role": 2
        },
        "entry_date_formatted": "04/04/2025 00:00:00",
        "departure_date_formatted": "None",
        "description": "trabajo para manuelita",
        "place": "manuelita",
        "entry_date": "2025-04-04T00:00:00Z",
        "departure_date": null,
        "state": 1
    },
    {
        "id": 2,
        "tools": [
            {
                "id": 1,
                "name": "Taladro",
                "code": "T-1",
                "state": 1,
                "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1743805307/afhimages/mnm6yun2cqcrp3a8rotl.jpg",
                "marca": "makita"
            },
            {
                "id": 2,
                "name": "Rodillo",
                "code": "R-1",
                "state": 1,
                "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1743805322/afhimages/wvo3gcuivn6mgffy1vef.jpg",
                "marca": "makita"
            }
        ],
        "receiver": {
            "id": 1,
            "user": {
                "username": "sebastianscarpetta19@gmail.com",
                "first_name": "sebastian",
                "last_name": "hernandez",
                "email": "sebastianscarpetta19@gmail.com"
            },
            "role": 1
        },
        "applicant": {
            "id": 2,
            "user": {
                "username": "sebastianscarpetta@gmail.com",
                "first_name": "sebastian",
                "last_name": "hernandez",
                "email": "sebastianscarpetta@gmail.com"
            },
            "role": 2
        },
        "entry_date_formatted": "06/04/2025 17:05:17",
        "departure_date_formatted": "None",
        "description": "trabajo para univalle",
        "place": "univalle",
        "entry_date": "2025-04-06T17:05:17.265283Z",
        "departure_date": null,
        "state": 3
    }
]

500 Internal Server Error

json

{
  "error": "Mensaje de error"
}
GET http://127.0.0.1:8000/ticket/ticket/<int:ticket_id>
Obtiene un ticket específico por su ID.

🔄 Parámetro en la URL:
ticket_id: ID del ticket que se desea consultar.

📤 Respuestas:
200 OK

json

{
    "id": 2,
    "tools": [
        {
            "id": 1,
            "name": "Taladro",
            "code": "T-1",
            "state": 1,
            "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1743805307/afhimages/mnm6yun2cqcrp3a8rotl.jpg",
            "marca": "makita"
        },
        {
            "id": 2,
            "name": "Rodillo",
            "code": "R-1",
            "state": 1,
            "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1743805322/afhimages/wvo3gcuivn6mgffy1vef.jpg",
            "marca": "makita"
        }
    ],
    "receiver": {
        "id": 1,
        "user": {
            "username": "sebastianscarpetta19@gmail.com",
            "first_name": "sebastian",
            "last_name": "hernandez",
            "email": "sebastianscarpetta19@gmail.com"
        },
        "role": 1
    },
    "applicant": {
        "id": 2,
        "user": {
            "username": "sebastianscarpetta@gmail.com",
            "first_name": "sebastian",
            "last_name": "hernandez",
            "email": "sebastianscarpetta@gmail.com"
        },
        "role": 2
    },
    "entry_date_formatted": "06/04/2025 17:05:17",
    "departure_date_formatted": "None",
    "description": "trabajo para univalle",
    "place": "univalle",
    "entry_date": "2025-04-06T17:05:17.265283Z",
    "departure_date": null,
    "state": 3
}
500 Internal Server Error

json
Copiar
Editar
{
  "error": "Mensaje de error"
}

PATCH (http://127.0.0.1:8000/ticket/changestate/)
Actualiza el estado de un ticket.

Body (JSON):
json

{
  "id": 1,        // ID del ticket
  "status": 2     // Nuevo estado (por ejemplo: 0 = Pendiente, 1 = En proceso, 2 = Resuelto)
}
📤 Respuestas:
200 OK

json
Copiar
Editar
{
  "message": "estado del ticket actualizado correctamente"
}
500 Internal Server Error

json
Copiar
Editar
{
  "error": "Mensaje de error"
}