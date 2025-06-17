
# 📄 API - Clientes

Esta documentación describe los endpoints disponibles para crear y actualizar información de clientes.

Base URL: http://127.0.0.1:8000/customer/

---

## 🧾 Crear Cliente

**URL:** `http://127.0.0.1:8000/customer/addcustomer/`  
**Método:** `POST`  
**Descripción:** Crea un nuevo cliente en el sistema.

### 🧑‍💻 Body (JSON)

```json
{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "3214567890",
  "post": "Gerente"
}
```

### ✅ Campos requeridos

| Campo   | Tipo   | Descripción                  |
|---------|--------|------------------------------|
| name    | string | Nombre completo del cliente  |
| email   | string | Correo electrónico           |
| phone   | string | Número de teléfono           |
| post    | string | Cargo del cliente            |

### 📤 Respuesta Exitosa (201)

```json
{
  "message": "Cliente creado exitosamente"
}
```

### ❌ Respuestas de Error

- **400** - Alguno de los campos requeridos no fue enviado

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

## ✏️ Actualizar Cliente

**URL:** `/updatecustomer/<int:customer_id>`  
**Método:** `PUT`  
**Descripción:** Actualiza la información de un cliente existente.

### 🧑‍💻 Body (JSON)

```json
{
  "name": "Juan Pérez",
  "email": "juan_nuevo@example.com",
  "phone": "3214567899",
  "post": "Director"
}
```

> ⚠️ Todos los campos son opcionales. Solo se actualizarán los que se envíen.

### ✅ Campos

| Campo   | Tipo   | Descripción                   |
|---------|--------|-------------------------------|
| name    | string | Nombre completo del cliente   |
| email   | string | Correo electrónico            |
| phone   | string | Número de teléfono            |
| post    | string | Cargo del cliente             |

### 📤 Respuesta Exitosa (200)

```json
{
  "message": "Cliente actualizado exitosamente"
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

- El `customer_id` debe ser un ID válido existente en la base de datos.
- Se recomienda validar los datos en el frontend antes de enviarlos.

---

🔹 3. Eliminar Cliente
Método: DELETE

URL: /delete/<int:customer_id>

Respuestas:

✅ 204 No Content


{ "message": "Cliente eliminado exitosamente" }
❌ 500 Internal Server Error


{ "error": "Mensaje del error" }
🔹 4. Obtener Todos los Clientes
Método: GET

URL: /getcustomers/

Respuestas:

✅ 200 OK


[
  {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "3123456789",
    "post": "Director"
  },
  ...
]
🔹 5. Obtener Cliente por ID
Método: GET

URL: /getcustomer/<int:customer_id>

Respuestas:

✅ 200 OK

json

{
  "id": 1,
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "3123456789",
  "post": "Director"
}
❌ 404 Not Found

json

{ "error": "Customer not found" }