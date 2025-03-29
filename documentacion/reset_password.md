Endpoint: http://127.0.0.1:8000/reset/request/

Método: POST

Descripción:
Este endpoint genera un código de recuperación de contraseña y lo envía al correo del usuario.

Parámetros:

email (string, requerido): Correo electrónico del usuario registrado.

Ejemplo de Petición:

{
    "email": "usuario@example.com"
}

Respuesta Exitosa (200):

{
    "message": "Código enviado al correo.",
    "Token": "abcd1234token"
}

Errores:

400: {"error": "Correo no encontrado."} (Si el correo no está registrado).

2. Validar Código de Recuperación

Endpoint: http://127.0.0.1:8000/reset/validate/

Método: POST

Descripción:
Verifica si un código de recuperación es válido y no ha expirado.

Parámetros:

code (string, requerido): Código de recuperación recibido por correo.

Ejemplo de Petición:

{
    "code": "1234"
}

Respuestas:

Exitosa (200): {"message": "codigo valido"}

Error (403): {"error": "el codigo de verificacion ya vencio"}

Error (500): {"error": "Mensaje de error interno"}

3. Restablecer Contraseña

Endpoint: http://127.0.0.1:8000/reset/reset/

Método: POST

Descripción:
Este endpoint permite cambiar la contraseña de un usuario autenticado.

Autenticación:
Se requiere un token de autenticación en el encabezado Authorization: Token <tu_token>.

Parámetros:

email (string, requerido): Correo electrónico del usuario.

new_password (string, requerido): Nueva contraseña a establecer.

Ejemplo de Petición:

{
    "email": "usuario@example.com",
    "new_password": "NuevaClaveSegura123"
}

Respuestas:

Exitosa (200): {"message": "La contrasena ha sido actualizada con exito"}

Error (400): {"error": "envia la contrasena nueva"}

Error (500): {"error": "Mensaje de error interno"}

