Endpoint: http://127.0.0.1:8000/auth/login/
Método: POST
Descripción: Permite autenticar a un usuario con su email y contraseña.

Solicitud (Request)

Headers:

Content-Type: application/json

Body (JSON):

{
  "email": "johndoe@example.com",
  "password": "securepassword"
}

Respuestas (Responses)

Éxito (200 OK):

{
  "token": "abcdef123456",
  "csrf_token": "xyz789",
  "role": "admin"
}

Error (400 Bad Request) - Falta email o contraseña:

{
  "error": "Email and password are required"
}

Error (401 Unauthorized) - Credenciales incorrectas:

{
  "error": "Invalid email or password"
}

3. Cierre de Sesión (Logout)

Endpoint: http://127.0.0.1:8000/auth/logout/
Método: POST
Descripción: Permite cerrar la sesión del usuario autenticado.

Solicitud (Request)

Headers:

Authorization: Token abcdef123456

Content-Type: application/json

Body: (Vacío)

Respuestas (Responses)

Éxito (200 OK):

{
  "message": "Logout exitoso"
}

Error (400 Bad Request) - Problema al cerrar sesión: