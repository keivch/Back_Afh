Crear Orden de Trabajo
▶️ Método: POST
📍 URL: (http://127.0.0.1:8000/workorder/create/)
📥 Cuerpo de la solicitud (application/json):

{
  "quote_id": 1,
  "start_date": "2025-06-20",
  "end_date": "2025-06-30",
  "description": "Instalación de tuberías",
  "workplace": "Planta Norte",
  "number_technicians": 2,
  "number_officers": 1,
  "number_auxiliaries": 3,
  "activity": "Instalación de redes hidráulicas",
  "permissions": ["ingreso_planta", "uso_equipos"]
}
📤 Respuesta exitosa (201):

{
  "message": "Orden de trabajo creada exitosamente",
  "id": 12
}
⚠️ Errores posibles:
400: Algún campo obligatorio no fue enviado.


{
  "error": "All fields are required"
}
500: Error interno (problema en el backend).


{
  "error": "Descripción del error"
}
🔄 Endpoint 2: Actualizar Orden de Trabajo
▶️ Método: PATCH
📍 URL: http://127.0.0.1:8000/workorder/update/<id>/

📥 Cuerpo de la solicitud (application/json):
Todos los campos son iguales a los del POST, pero puedes enviar solo los que quieras actualizar (aunque tu servicio parece requerirlos todos).


{
  "quote_id": 1,
  "start_date": "2025-06-21",
  "end_date": "2025-07-01",
  "description": "Instalación actualizada",
  "workplace": "Planta Norte",
  "number_technicians": 4,
  "number_officers": 2,
  "number_auxiliaries": 2,
  "activity": "Cambio de actividad",
  "permissions": ["ingreso_planta", "uso_grúa"]
}
📤 Respuesta exitosa (200):

{
  "message": "Orden de trabajo actualizada exitosamente",
  "id": 12
}
⚠️ Errores posibles:
500: Error interno del servidor


{
  "error": "Descripción del error"
}
🧾 Lista de campos esperados:
Campo	Tipo	Requerido	Descripción
quote_id	integer	✅ Sí	ID de la cotización relacionada
start_date	string	✅ Sí	Fecha de inicio (YYYY-MM-DD)
end_date	string	❌ Opcional	Fecha de fin (YYYY-MM-DD)
description	string	✅ Sí	Descripción general de la orden
workplace	string	✅ Sí	Lugar donde se hará el trabajo
number_technicians	integer	✅ Sí	Número de técnicos asignados
number_officers	integer	✅ Sí	Número de oficiales
number_auxiliaries	integer	✅ Sí	Número de auxiliares
activity	string	✅ Sí	Actividad principal de la orden
permissions	list	✅ Sí	Permisos necesarios (lista de strings)






GET (http://127.0.0.1:8000/workorder/workorders/)
Descripción
Obtiene una lista de todas las órdenes de trabajo registradas.

Respuesta exitosa (200 OK)

[
   {
  "id": 1,
  "quote": {
    "id": 27,
    "code": "1-2025",
    "customer": {
      "id": 1,
      "name": "serenity sas",
      "email": "serenity@gmail.com",
      "phone": "12345678",
      "post": null
    },
    "description": "construccion",
    "issue_date": "2025-06-19",
    "state": 1,
    "options": {
      "id": 10,
      "name": "pruebis",
      "total_value": "504192.00",
      "total_value_formatted": "$504.192",
      "items": [
        {
          "id": 12,
          "description": "cemento",
          "units": "m2",
          "amount": 3,
          "unit_value": "130000.00",
          "total_value": "390000.00",
          "unit_value_formatted": "$130.000",
          "total_value_formatted": "$390.000"
        }
      ],
      "subtotal": "$390.000"
    },
    "tasks": [
      "hacer aseo",
      "juen es puta"
    ],
    "iva": "0.19",
    "utility": "0.00",
    "unforeseen": "0.00",
    "administration": "0.00",
    "revision": 1,
    "construction": null,
    "iva_value": "$74.100",
    "utility_value": "$0",
    "unforeseen_value": "$0",
    "administration_value": "$0",
    "method_of_payment": "efectivo mi papacho "
  },
  "start_date": "2025-06-01",
  "end_date": "2025-06-10",
  "description": "Mantenimiento general",
  "workplace": 2,
  "number_technicians": 3,
  "number_officers": 2,
  "number_auxiliaries": 1,
  "activity": 1,
  "permissions": [
    "Trabajo en alturas",
    "Ats"
  ]
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
  "id": 1,
  "quote": {
    "id": 27,
    "code": "1-2025",
    "customer": {
      "id": 1,
      "name": "serenity sas",
      "email": "serenity@gmail.com",
      "phone": "12345678",
      "post": null
    },
    "description": "construccion",
    "issue_date": "2025-06-19",
    "state": 1,
    "options": {
      "id": 10,
      "name": "pruebis",
      "total_value": "504192.00",
      "total_value_formatted": "$504.192",
      "items": [
        {
          "id": 12,
          "description": "cemento",
          "units": "m2",
          "amount": 3,
          "unit_value": "130000.00",
          "total_value": "390000.00",
          "unit_value_formatted": "$130.000",
          "total_value_formatted": "$390.000"
        }
      ],
      "subtotal": "$390.000"
    },
    "tasks": [
      "hacer aseo",
      "juen es puta"
    ],
    "iva": "0.19",
    "utility": "0.00",
    "unforeseen": "0.00",
    "administration": "0.00",
    "revision": 1,
    "construction": null,
    "iva_value": "$74.100",
    "utility_value": "$0",
    "unforeseen_value": "$0",
    "administration_value": "$0",
    "method_of_payment": "efectivo mi papacho "
  },
  "start_date": "2025-06-01",
  "end_date": "2025-06-10",
  "description": "Mantenimiento general",
  "workplace": 2,
  "number_technicians": 3,
  "number_officers": 2,
  "number_auxiliaries": 1,
  "activity": 1,
  "permissions": [
    "Trabajo en alturas",
    "Ats"
  ]
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


