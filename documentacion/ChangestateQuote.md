API de Clientes
Base URL: http://127.0.0.1:8000/quote/{id quote}



🔹 actualizar estado
Método: PATCH

URL: /addcustomer/


Body:


{
  "state": [1, 2 o 3]
}
Respuestas:

✅ 200 ok

{
    "message": "Estado de la cotizacion actualizado exitosamente"
}
❌ 400 Bad Request – Campos faltantes


{ "error": "All fields are required" }


Al cambiar el estado a aprobada crea la orden de trabajo automaticamente