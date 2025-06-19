# 📄 API - Certificados de Entrega

Documentación de los endpoints para gestionar certificados de entrega en el sistema.

> 🧩 URL base: `http://127.0.0.1:8000/deliverycertificate`

---

## ➕ Crear Certificado de Entrega

**URL:** `POST /create/`  
**Descripción:** Crea un nuevo certificado de entrega asociando observaciones, recomendaciones y exhibits.

### 📥 Body (JSON)

```json
{
  "work_order_id": 12,
  "observations": "Todo fue entregado según lo acordado.",
  "recommendations": "Evitar el contacto con agua.",
  "exhibit_ids": [1, 2],
  " development": "ola",
  " description": "olax2"
}
✅ Campos Requeridos
Campo	Tipo	Requerido	Descripción
work_order_id	integer	✅ Sí	ID de la orden de trabajo asociada
observations	string	✅ Sí	Observaciones del técnico
recommendations	string	✅ Sí	Recomendaciones para el cliente
exhibit_ids	array	❌ No	Lista de IDs de exhibits asociados

📤 Respuesta Exitosa (201)

{
  "message": "Certificado de entrega creado exitosamente"
}
❌ Errores
400 – Datos requeridos no enviados

500 – Error interno del servidor

✏️ Actualizar Certificado de Entrega
URL: PATCH /update/<id>/
Descripción: Actualiza las observaciones y/o recomendaciones de un certificado existente.

📥 Body (JSON)

{
  "observations": "Nueva observación",
  "recommendations": "Nueva recomendación"
}
⚠️ Debes enviar al menos uno de los dos campos.

📤 Respuesta Exitosa (200)
json
Copiar
Editar
{
  "message": "Certificado de entrega actualizado exitosamente"
}
❌ Errores
400 – No se envió ninguna observación ni recomendación

500 – Error interno del servidor

📋 Obtener Todos los Certificados
URL: GET /get/
Descripción: Devuelve una lista de todos los certificados de entrega existentes.

📤 Respuesta Exitosa (200)

[
  {
    "id": 1,
    "work_order": {
      "id": 5,
      "Quotes": {
        "id": 9,
        "code": "1-2025",
        "customer": {
          "id": 1,
          "name": "serenity sas",
          "email": "serenity@gmail.com",
          "phone": "12345678",
          "post": null
        },
        "description": "oliwis",
        "issue_date": "2025-06-16",
        "state": 2,
        "options": {
          "id": 5,
          "name": "prueba",
          "total_value": "1113660.00",
          "total_value_formatted": "$1.113.660",
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
            },
            {
              "id": 7,
              "description": "popeye",
              "units": "Milímetros",
              "amount": 2,
              "unit_value": "12000.00",
              "total_value": "24000.00",
              "unit_value_formatted": "$12.000",
              "total_value_formatted": "$24.000"
            }
          ],
          "subtotal": "$414.000"
        },
        "tasks": [
          "hacer aseo",
          "juen es puta"
        ],
        "iva": "0.19",
        "utility": "0.50",
        "unforeseen": "0.50",
        "administration": "0.50",
        "revision": 5,
        "construction": "",
        "iva_value": "$39.330",
        "utility_value": "$207.000",
        "unforeseen_value": "$207.000",
        "administration_value": "$207.000",
        "method_of_payment": "efectivo mi papacho "
      },
      "start_date": "2025-06-17",
      "end_date": "2025-06-17"
    },
    "exhibit": [
      {
        "id": 1,
        "tittle": "formacion",
        "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1750277910/afhimages/b9wzeob5olwcvjfr65xg.jpg"
      }
    ],
    "date": "2025-06-18",
    "observations": "ola",
    "recommendations": "uwu"
  }
]
❌ Errores
500 – Error interno del servidor

🔎 Obtener Certificado por ID
URL: GET /get/<id>/
Descripción: Devuelve la información de un certificado específico por su ID.

📤 Respuesta Exitosa (200)

Editar
{
  "id": 1,
  "work_order": {
    "id": 5,
    "Quotes": {
      "id": 9,
      "code": "1-2025",
      "customer": {
        "id": 1,
        "name": "serenity sas",
        "email": "serenity@gmail.com",
        "phone": "12345678",
        "post": null
      },
      "description": "oliwis",
      "issue_date": "2025-06-16",
      "state": 2,
      "options": {
        "id": 5,
        "name": "prueba",
        "total_value": "1113660.00",
        "total_value_formatted": "$1.113.660",
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
          },
          {
            "id": 7,
            "description": "popeye",
            "units": "Milímetros",
            "amount": 2,
            "unit_value": "12000.00",
            "total_value": "24000.00",
            "unit_value_formatted": "$12.000",
            "total_value_formatted": "$24.000"
          }
        ],
        "subtotal": "$414.000"
      },
      "tasks": [
        "hacer aseo",
        "juen es puta"
      ],
      "iva": "0.19",
      "utility": "0.50",
      "unforeseen": "0.50",
      "administration": "0.50",
      "revision": 5,
      "construction": "",
      "iva_value": "$39.330",
      "utility_value": "$207.000",
      "unforeseen_value": "$207.000",
      "administration_value": "$207.000",
      "method_of_payment": "efectivo mi papacho "
    },
    "start_date": "2025-06-17",
    "end_date": "2025-06-17"
  },
  "exhibit": [
    {
      "id": 1,
      "tittle": "formacion",
      "image": "https://res.cloudinary.com/dp4tvthea/image/upload/v1750277910/afhimages/b9wzeob5olwcvjfr65xg.jpg"
    }
  ],
  "date": "2025-06-18",
  "observations": "ola",
  "recommendations": "uwu"
}
❌ Errores
404 – Certificado de entrega no encontrado

500 – Error interno del servidor

➕ Agregar Exhibit a Certificado
URL: PATCH /add-exhibit/<delivery_certificate_id>/<exhibit_id>/
Descripción: Asocia un exhibit existente a un certificado de entrega.

📤 Respuesta Exitosa (200)

❌ Errores
404 – Certificado de entrega o exhibit no encontrado

500 – Error interno del servidor










