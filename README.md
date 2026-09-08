[README.md](https://github.com/user-attachments/files/31931820/README.md)
# 🌍 GeoWeather SaaS

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=Leaflet&logoColor=white)

**GeoWeather SaaS** es una aplicación web interactiva desarrollada con **FastAPI** y **SQLite** que permite consultar métricas del clima en tiempo real utilizando geolocalización dinámica y mapas interactivos. Ofrece autenticación de usuarios con sesiones cifradas, selección directa en el mapa por coordenadas (*reverse geocoding*) y guardado de puntos favoritos.

---

## 🔥 Características Principales

- 🔐 **Autenticación Completa de Usuarios**: Registro, inicio de sesión y gestión de sesiones mediante middleware seguro cifrado en cookies.
- 🗺️ **Mapa Interactivo (Leaflet.js)**: Haz clic en cualquier coordenadas del mapa para consultar el clima exacto de esa ubicación en vivo (*Reverse Geocoding*).
- 🔍 **Búsqueda por Ciudad**: Motor de geocodificación que permite encontrar cualquier ciudad del mundo.
- ⭐ **Lugares Favoritos**: Guarda ubicaciones frecuentes en tu panel personal para consultarlas con un solo clic.
- ⚡ **API Meteorológica**: Integración con [Open-Meteo API](https://open-meteo.com/) para métricas de temperatura, sensación térmica, humedad y velocidad del viento.
- 🎨 **Interfaz Glassmorphism**: Diseño oscuro y moderno totalmente responsivo desarrollado con Bootstrap 5 y FontAwesome.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.10+, FastAPI, Starlette `SessionMiddleware`, Uvicorn.
- **Base de Datos & ORM**: SQLite3, SQLAlchemy.
- **Frontend & Plantillas**: Jinja2 Templates, Bootstrap 5, FontAwesome 6, JavaScript ES6 (Fetch API).
- **Mapas y Geolocalización**: Leaflet.js, OpenStreetMap (Nominatim Reverse Geocoding).
- **Cliente HTTP**: `httpx` para peticiones asíncronas.

---

## 🚀 Instalación y Configuración Local

### Prerrequisitos

Asegúrate de tener instalado **Python 3.9+** en tu sistema.

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/AngelLisandro2024/geoweather-saas.git
   cd geoweather-saas
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   # En Linux / macOS:
   python3 -m venv venv
   source venv/bin/activate

   # En Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install fastapi uvicorn sqlalchemy starlette httpx passlib bcrypt jinja2 python-multipart
   ```

4. **Ejecutar el servidor de desarrollo:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Acceder a la aplicación:**
   Abre tu navegador web e ingresa a `http://127.0.0.1:8000`.

---

## 📂 Estructura del Proyecto

```text
geoweather-saas/
├── database.py       # Configuración de SQLAlchemy y motor SQLite
├── models.py         # Modelos de base de datos (User, FavoriteLocation)
├── auth.py           # Hashing y verificación de contraseñas
├── main.py           # Rutas de FastAPI, controladores y endpoints
├── static/           # Archivos estáticos (CSS custom, imágenes)
└── templates/        # Plantillas HTML renderizadas con Jinja2
    ├── base.html     # Layout base con CDN y navbar
    ├── login.html    # Formulario de inicio de sesión
    ├── register.html # Formulario de registro de usuario
    └── dashboard.html# Panel principal con buscador, mapa y favoritos
```

---

## 🔌 Endpoints de la API

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Vista principal del Dashboard. |
| `GET` | `/api/weather?ciudad={nombre}` | Consulta clima por nombre de ciudad. |
| `GET` | `/api/weather?lat={lat}&lon={lon}` | Consulta clima por coordenadas del mapa. |
| `POST` | `/api/favorites/add` | Agrega la ubicación actual a los favoritos del usuario. |

---

## 🛡️ Archivo `.gitignore` Recomendado

Para evitar subir la base de datos local, el entorno virtual o archivos temporales a GitHub, crea un archivo llamado `.gitignore` en la raíz con el siguiente contenido:

```text
# Entorno virtual
venv/
env/
.venv/

# Base de datos SQLite
*.db
*.sqlite3

# Caché de Python
__pycache__/
*.py[cod]

# Entorno e IDE
.vscode/
.idea/
.env
```

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Libre para uso, modificación y distribución.
