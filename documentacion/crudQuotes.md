# 📄 API - Cotizaciones

Esta documentación describe los endpoints disponibles para crear y actualizar cotizaciones.
Base URL: http://127.0.0.1:8000/quote/

---

## ➕ Crear Cotización

**URL:** `/addquote/`  
**Método:** `POST`  
**Descripción:** Crea una nueva cotización en el sistema.

### 🧑‍💻 Body (JSON)

```json
{
  "description": "Instalación eléctrica completa",
  "customer_id": 1,
  "options": 2,
  "tasks": [
    "ostia tio joder", "flipas chaval"
  ],
  "utility": 0.10,
  "unforeseen": 0.05,
  "administration": 0.03,
  "method_of_payment": "ojito tilin",
  "construction": "jaramillo mora"
}
```

### ✅ Campos requeridos

| Campo             | Tipo     | Descripción                                           |
|------------------|----------|-------------------------------------------------------|
| description       | string   | Descripción general de la cotización                  |
| customer_id       | integer  | ID del cliente asociado                               |
| options           | integer  | ID de la opción seleccionada                          |
| tasks             | array    | Lista de tareas a realizar  |     |
| utility           | float    | Porcentaje de utilidad       (se envia si y solo si es para constructora)                        
| unforeseen        | float    | Porcentaje de imprevistos    (se envia si y solo si es para constructora)                               
| administration    | float    | Porcentaje de administración  (se envia si y solo si es para constructora)
  construction      | string   | nombre constructora ((se envia si y solo si es para constructora))                
| method_of_payment | string   | Método de pago 
### 📤 Respuesta Exitosa (201)

```json
{
  "message": "Cotización creada exitosamente"
}
```

### ❌ Respuestas de Error

- **400** - Faltan campos obligatorios

```json
{
  "error": "All fields are required"
}
```

- **500** - Error interno del servidor

```json
{
  "error": "Descripción del error"
}
```

---

## ✏️ Actualizar Cotización

**URL:** /updatequote/<int:quote_id>
**Método:** `PUT`  
**Descripción:** Actualiza los datos de una cotización existente.

### 🧑‍💻 Body (JSON)

```json
{
  "description": "Actualización de cableado",
  "customer_id": 1,
  "options": 3,
  "tasks": [
    "flipo"
  ],
  "iva": 0.19,
  "utility": 0.12,
  "unforeseen": 0.06,
  "administration": 0.04,
  "method_of_payment": "Crédito"
}
```

> ⚠️ Todos los campos son opcionales, pero si no se especifican, se dejarán como `null` (excepto el IVA que por defecto será `0.19`).

### ✅ Campos

| Campo             | Tipo     | Descripción                                           |
|------------------|----------|-------------------------------------------------------|
| description       | string   | Descripción general de la cotización                  |
| customer_id       | integer  | ID del cliente asociado                               |
| options           | integer  | ID de la opción seleccionada                          |
| tasks             | array    | Lista de tareas a realizar                            |
| iva               | float    | Porcentaje de IVA (default: 0.19)                     |
| utility           | float    | Porcentaje de utilidad                                |
| unforeseen        | float    | Porcentaje de imprevistos                             |
| administration    | float    | Porcentaje de administración                          |
| method_of_payment | string   | Método de pago                                        |

### 📤 Respuesta Exitosa (200)

```json
{
  "message": "Cotizacion actualizada exitosamente"
}
```

### ❌ Respuestas de Error

- **500** - Error interno del servidor

```json
{
  "error": "Descripción del error"
}
```

---

## 📌 Notas

- El `quote_id` debe ser un ID válido de una cotización existente.
- Asegúrate de validar los datos correctamente en el frontend.

---

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
    "state": 1,
    "options": {
      "id": 5,
      "name": "prueba",
      "total_value": "1012050.00",
      "total_value_formatted": "$1.012.050",
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
      ],
      "subtotal": "$390.000"
    },
    "tasks": [
      "hacer aseo",
      "juen es puta"
    ],
    "iva": "0.19",
    "utility": "0.50",
    "unforeseen": "0.50",
    "administration": "0.50",
    "revision": 1,
    "construction": "",
    "iva_value": "$37.050",
    "utility_value": "$195.000",
    "unforeseen_value": "$195.000",
    "administration_value": "$195.000",
    "method_of_payment": "efectivo mi papacho "
  }
]
🔹 5. Obtener Cotización por ID
Método: GET

URL: /getquote/<int:quote_id>

Respuestas:

✅ 200 OK

json

{
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
    "state": 1,
    "options": {
      "id": 5,
      "name": "prueba",
      "total_value": "1012050.00",
      "total_value_formatted": "$1.012.050",
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
      ],
      "subtotal": "$390.000"
    },
    "tasks": [
      "hacer aseo",
      "juen es puta"
    ],
    "iva": "0.19",
    "utility": "0.50",
    "unforeseen": "0.50",
    "administration": "0.50",
    "revision": 1,
    "construction": "",
    "iva_value": "$37.050",
    "utility_value": "$195.000",
    "unforeseen_value": "$195.000",
    "administration_value": "$195.000",
    "method_of_payment": "efectivo mi papacho "
  }
❌ 500 Internal Server Error

json

{ "error": "Mensaje del error" }