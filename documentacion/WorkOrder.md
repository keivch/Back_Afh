GET (http://127.0.0.1:8000/workorder/workorders/)
Descripción
Obtiene una lista de todas las órdenes de trabajo registradas.

Respuesta exitosa (200 OK)

[
    {
        "id": 3,
        "Quotes": {
            "id": 1,
            "customer": {
                "id": 1,
                "name": "serenity sas",
                "email": "serenity@gmail.com",
                "phone": "12345678",
                "post": null
            },
            "options": {
                "id": 1,
                "name": "pruebis",
                "total_value": "390000.00",
                "total_value_formatted": "$390.000",
                "items": [
                    {
                        "id": 1,
                        "description": "logica",
                        "units": "cm2",
                        "amount": 3,
                        "unit_value": "130000.00",
                        "total_value": "390000.00",
                        "unit_value_formatted": "$130.000",
                        "total_value_formatted": "$390.000"
                    }
                ]
            },
            "code": "1-2025",
            "description": "trabajo",
            "issue_date": "2025-06-16",
            "state": 1,
            "tasks": [
                "lavar"
            ],
            "iva": "0.19",
            "utility": "0.00",
            "unforeseen": "0.00",
            "administration": "0.00",
            "revision": 1,
            "construction": null
        },
        "start_date": "2025-06-16",
        "end_date": "2025-06-20"
    },
    {
        "id": 4,
        "Quotes": {
            "id": 2,
            "customer": {
                "id": 1,
                "name": "serenity sas",
                "email": "serenity@gmail.com",
                "phone": "12345678",
                "post": null
            },
            "options": {
                "id": 3,
                "name": "Construccion cubierta nueva",
                "total_value": "110271000.00",
                "total_value_formatted": "$110.271.000",
                "items": [
                    {
                        "id": 3,
                        "description": "Suministro e instalación de estructura metálica en viga IPE 200mm, viga IPE 100mm, PHR 220mmx 80mm x 2mm, según plano ",
                        "units": "Metros",
                        "amount": 413,
                        "unit_value": "185000.00",
                        "total_value": "76405000.00",
                        "unit_value_formatted": "$185.000",
                        "total_value_formatted": "$76.405.000"
                    },
                    {
                        "id": 4,
                        "description": "Suministro e instalación de cubierta en teja arquitectónica pintada incluye accesorios de fijación y caballete ",
                        "units": "Metros",
                        "amount": 413,
                        "unit_value": "82000.00",
                        "total_value": "33866000.00",
                        "unit_value_formatted": "$82.000",
                        "total_value_formatted": "$33.866.000"
                    }
                ]
            },
            "code": "2-2025",
            "description": "trabajo 2",
            "issue_date": "2025-06-16",
            "state": 1,
            "tasks": [
                "juan"
            ],
            "iva": "0.19",
            "utility": "0.00",
            "unforeseen": "0.00",
            "administration": "0.00",
            "revision": 1,
            "construction": null
        },
        "start_date": "2025-06-16",
        "end_date": "2025-06-26"
    }
]

Errores posibles
500 Internal Server Error: Si ocurre un error inesperado en el servidor.

📄 API: Obtener una orden de trabajo por ID
Endpoint
bash
Copiar
Editar
GET  (http://127.0.0.1:8000/workorder/workorder/<id>)
Parámetros
id (path): ID numérico de la orden de trabajo.

Descripción
Obtiene la información detallada de una orden de trabajo específica.

Ejemplo

GET 
Respuesta exitosa (200 OK)

{
    "id": 3,
    "Quotes": {
        "id": 1,
        "customer": {
            "id": 1,
            "name": "serenity sas",
            "email": "serenity@gmail.com",
            "phone": "12345678",
            "post": null
        },
        "options": {
            "id": 1,
            "name": "pruebis",
            "total_value": "390000.00",
            "total_value_formatted": "$390.000",
            "items": [
                {
                    "id": 1,
                    "description": "logica",
                    "units": "cm2",
                    "amount": 3,
                    "unit_value": "130000.00",
                    "total_value": "390000.00",
                    "unit_value_formatted": "$130.000",
                    "total_value_formatted": "$390.000"
                }
            ]
        },
        "code": "1-2025",
        "description": "trabajo",
        "issue_date": "2025-06-16",
        "state": 1,
        "tasks": [
            "lavar"
        ],
        "iva": "0.19",
        "utility": "0.00",
        "unforeseen": "0.00",
        "administration": "0.00",
        "revision": 1,
        "construction": null
    },
    "start_date": "2025-06-16",
    "end_date": "2025-06-20"
}
Errores posibles
404 Not Found: Si la orden de trabajo con el ID especificado no existe.


{
  "error": "Work order not found"
}
500 Internal Server Error: Si ocurre un error inesperado.


## 1. Descargar PDF de Cotización

**Endpoint:** `GET http://127.0.0.1:8000/workorder/pdf/<id_workorder>/`  
**Descripción:** Genera y devuelve un archivo PDF descargable con la información de la cotización asociada a una orden de trabajo.

### Parámetros de Ruta
- `id_workorder` (int): ID de la orden de trabajo. Obligatorio.

### Respuesta Exitosa (HTTP 200)
- Devuelve un archivo PDF (`Content-Disposition: attachment`) con el nombre: `Orden-<código de cotización>.pdf`.

### Respuesta de Error (HTTP 400/500)
```json
// Si falta el ID de la orden de trabajo
{
  "error": "Id de la cotizacion es requerido"
}

// Si ocurre un error inesperado
{
  "error": "<mensaje de error>"
}
```

---

## 2. Finalizar Orden de Trabajo

**Endpoint:** `PATCH http://127.0.0.1:8000/workorder/finish/<int:id>/`  
**Descripción:** Marca una orden de trabajo como finalizada.

### Parámetros de Ruta
- `id` (int): ID de la orden de trabajo. Obligatorio.

### Respuesta Exitosa (HTTP 200)
```json
{
  "message": "Orden de trabajo finalizada exitosamente"
}
```

### Respuesta de Error (HTTP 400/500)
```json
// Si falta el ID
{
  "error": "Id de la orden de trabajo es requerido"
}

// Si ocurre un error inesperado
{
  "error": "<mensaje de error>"
}
```

