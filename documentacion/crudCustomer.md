API de Clientes
Base URL: http://127.0.0.1:8000/customer/



🔹 1. Crear Cliente
Método: POST

URL: /addcustomer/


Body:


{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "phone": "3123456789"
}
Respuestas:

✅ 201 Created

{ "message": "Cliente creado exitosamente" }
❌ 400 Bad Request – Campos faltantes


{ "error": "All fields are required" }
🔹 2. Actualizar Cliente
Método: PUT

URL: /updatecustomer/<int:customer_id>



Body (solo lo que se vaya a editar, no toda la info):

json

{
  "name": "Carlos Torres",
  "email": "carlos@example.com",
  "phone": "3009876543"
}
Respuestas:

✅ 200 OK

json

{ "message": "Cliente actualizado exitosamente" }
❌ 500 Internal Server Error


{ "error": "Mensaje del error" }
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

json
Copiar
Editar
[
  {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "3123456789"
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
  "phone": "3123456789"
}
❌ 404 Not Found

json

{ "error": "Customer not found" }