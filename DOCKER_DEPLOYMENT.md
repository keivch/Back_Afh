# Guía de Despliegue con Docker

## Archivos creados para Docker

- `Dockerfile`: Configuración del contenedor de la aplicación
- `docker-compose.yml`: Orquestación de servicios (app + base de datos)
- `docker-compose.dockploy.yml`: Configuración específica para Dockploy
- `.dockploy.yml`: Configuración de despliegue automático con Dockploy
- `.dockerignore`: Archivos a excluir del contexto de Docker

## Variables de entorno necesarias

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
BACKURL=http://localhost:8000
FRONT_URL=http://localhost:3000

# Database Settings
URL_DB=postgresql://afh_user:afh_password@db:5432/afh_db
POSTGRES_DB=afh_db
POSTGRES_USER=afh_user
POSTGRES_PASSWORD=afh_password

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cloudinary Settings
CLOUD_NAME=your-cloud-name
API_KEY=your-api-key
API_SECRET=your-api-secret

# Pusher Settings
APP_ID=your-app-id
KEY=your-key
SECRET=your-secret
CLUSTER=your-cluster
```

## Comandos para ejecutar

### 1. Construir y ejecutar con Docker Compose
```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build
```

### 2. Ejecutar migraciones
```bash
# Ejecutar migraciones en el contenedor
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### 3. Recopilar archivos estáticos
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### 4. Comandos útiles
```bash
# Ver logs
docker-compose logs -f web

# Acceder al shell del contenedor
docker-compose exec web bash

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

## Características del Dockerfile

- **Imagen base**: Python 3.11-slim
- **Dependencias del sistema**: Incluye todas las librerías necesarias para WeasyPrint, Pillow, y PostgreSQL
- **Seguridad**: Ejecuta con usuario no-root
- **Optimización**: Usa .dockerignore para excluir archivos innecesarios
- **Servidor**: Gunicorn con 3 workers

## Estructura de volúmenes

- `postgres_data`: Datos de la base de datos PostgreSQL
- `static_volume`: Archivos estáticos de Django
- `media_volume`: Archivos de media subidos por usuarios

## Puertos

- **8000**: Aplicación Django
- **5432**: Base de datos PostgreSQL

## Despliegue con Dockploy

### Configuración de Dockploy

El archivo `.dockploy.yml` está configurado para despliegue automático con las siguientes características:

- **Health checks**: Verificación automática del estado de la aplicación
- **Recursos limitados**: 1GB RAM y 0.5 CPU
- **Reinicio automático**: `unless-stopped`
- **Logs rotativos**: Máximo 10MB por archivo, 3 archivos
- **Traefik**: Configuración automática de proxy reverso y SSL

### Variables de entorno adicionales para Dockploy

Agrega estas variables a tu archivo `.env`:

```env
# Dockploy specific
DOMAIN=your-domain.com
POSTGRES_DB=afh_db
POSTGRES_USER=afh_user
POSTGRES_PASSWORD=your-secure-password
```

### Comandos de Dockploy

```bash
# Desplegar con Dockploy
dockploy deploy

# Ver logs en tiempo real
dockploy logs -f

# Reiniciar la aplicación
dockploy restart

# Ver estado de los servicios
dockploy ps
```

## Notas importantes

1. Asegúrate de tener Docker y Docker Compose instalados
2. Para Dockploy, asegúrate de tener la configuración correcta del dominio
3. Configura todas las variables de entorno antes de ejecutar
4. Para producción, cambia `DEBUG=False` y configura `ALLOWED_HOSTS` apropiadamente
5. Los archivos estáticos y media se persisten en volúmenes Docker
6. Dockploy manejará automáticamente las migraciones y la recolección de archivos estáticos
