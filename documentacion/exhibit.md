# 📄 API - Exhibits

Documentación de los endpoints para gestionar "exhibits" en el sistema.

> 🧩 URL base: `http://127.0.0.1:8000/exhibit`

---

## ➕ Crear Exhibit

**URL:** `POST /create/`  
**Descripción:** Crea un nuevo exhibit con título e imagen.

### Body (form-data)

| Campo  | Tipo     | Requerido | Descripción                     |
|--------|----------|-----------|---------------------------------|
| tittle | string   | ✅ Sí      | Título del exhibit              |
| image  | file     | ❌ No      | Imagen asociada al exhibit      |

### Respuesta Exitosa (201)

```json
{
  "message": "Exhibit created successfully"
}
```

### Respuesta de Error

- **400** – Faltan campos obligatorios

```json
{
  "error": "El título es requerido"
}
```

- **500** – Error interno

```json
{
  "error": "Descripción del error"
}
```

---

## ✏️ Actualizar Exhibit

**URL:** `PATCH /update/<id>/`  
**Descripción:** Actualiza el título o la imagen de un exhibit existente.

### Body (form-data)

| Campo  | Tipo   | Requerido | Descripción                        |
|--------|--------|-----------|------------------------------------|
| title  | string | ❌ No      | Nuevo título del exhibit           |
| image  | file   | ❌ No      | Nueva imagen del exhibit           |

> ⚠️ Se debe enviar al menos uno de los dos campos (`title` o `image`).

### Respuesta Exitosa (200)

```json
{
  "message": "Exhibit updated successfully"
}
```

### Respuestas de Error

- **400** – No se envió ningún campo para actualizar

```json
{
  "error": "Debe proporcionar al menos un título o una imagen"
}
```

- **404** – Exhibit no encontrado

```json
{
  "error": "Exhibit not found"
}
```

- **500** – Error interno

```json
{
  "error": "Descripción del error"
}
```

---

## 📋 Obtener Todos los Exhibits

**URL:** `GET /get/`  
**Descripción:** Devuelve una lista de todos los exhibits disponibles.

### Respuesta Exitosa (200)

```json
[
  {
    "id": 1,
    "title": "Ejemplo",
    "image": "http://ruta.imagen/archivo.jpg"
  },
  ...
]
```

### Respuesta de Error (500)

```json
{
  "error": "Descripción del error"
}
```

---

## 🔎 Obtener Exhibit por ID

**URL:** `GET /get/<id>/`  
**Descripción:** Devuelve los datos de un exhibit específico por su ID.

### Respuesta Exitosa (200)

```json
{
  "id": 1,
  "title": "Ejemplo",
  "image": "http://ruta.imagen/archivo.jpg"
}
```

### Respuesta de Error

- **404** – Exhibit no encontrado

```json
{
  "error": "Exhibit not found"
}
```

- **500** – Error interno

```json
{
  "error": "Descripción del error"
}
```

---