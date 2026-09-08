# 🌍 GeoWeather SaaS

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=for-the-badge&logo=Leaflet&logoColor=white)

**GeoWeather SaaS** es una aplicación web interactiva que permite consultar métricas del clima en tiempo real utilizando geolocalización dinámica y mapas interactivos. Construida sobre FastAPI y SQLite, ofrece autenticación de usuarios, gestión de ubicación por mapa interactivo y guardado de puntos favoritos.

---

## 🔥 Características Principales

- 🔐 **Autenticación Completa de Usuarios**: Registro, inicio de sesión y gestión de sesiones mediante middleware seguro cifrado en cookies.
- 🗺️ **Mapa Interactivo (Leaflet.js)**: Haz clic en cualquier coordenadas del mapa para consultar el clima exacto de esa ubicación en vivo (*Reverse Geocoding*).
- 🔍 **Búsqueda por Ciudad**: Motor de geocodificación que permite encontrar cualquier ciudad del mundo.
- ⭐ **Lugares Favoritos**: Guarda ubicaciones frecuentes en tu panel personal para consultarlas con un solo clic.
- ⚡ **API Meteorológica**: Integración con [Open-Meteo API](https://open-meteo.com/) (sin límite de req) para métricas de temperatura, sensación térmica, humedad y velocidad del viento.
- 🎨 **Interfaz Glassmorphism**: Diseño oscuro y moderno responsivo desarrollado con Bootstrap 5 y FontAwesome.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.10+, FastAPI, Starlette SessionMiddleware.
- **Base de Datos & ORM**: SQLite3, SQLAlchemy.
- **Frontend & Plantillas**: Jinja2 Templates, Bootstrap 5, FontAwesome 6, JavaScript ES6 (Fetch API).
- **Mapas y Geolocalización**: Leaflet.js, OpenStreetMap (Nominatim Reverse Geocoding).
- **Cliente HTTP**: `httpx` para peticiones asíncronas.

---

## 🚀 Instalación y Configuración Local

### Prerequisitos

Asegúrate de tener instalado Python 3.9 o superior en tu sistema.

### Pasos

1. **Clona el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/geoweather-saas.git](https://github.com/tu-usuario/geoweather-saas.git)
   cd geoweather-saas
Crea un entorno virtual:Bashpython -m venv venv

source venv/bin/activate  # En Linux/macOS

# venv\Scripts\activate   # En Windows

Instala las dependencias necesarias:Bashpip install fastapi uvicorn sqlalchemy starlette httpx passlib bcrypt jinja2 python-multipart

Ejecuta el servidor de desarrollo:Bashuvicorn main:app --reload

Abre en el navegador:Visita http://127.0.0.1:8000 en tu navegador web.

📂 Estructura del ProyectoPlaintextgeoweather-saas/
├── database.py       # Configuración de SQLAlchemy y motor SQLite
├── models.py         # Modelos de BD (User, FavoriteLocation)
├── auth.py           # Funciones de hashing y verificación de contraseñas
├── main.py           # Rutas de la API, controladores y endpoints
├── static/           # Archivos estáticos (CSS custom, imágenes)
└── templates/        # Plantillas HTML con Jinja2
    ├── base.html
    ├── login.html
    ├── register.html
    └── dashboard.html
    
🔌 Endpoints de la APIMétodoRutaDescripciónGET/Vista principal del Dashboard.GET/api/weather?ciudad={nombre}Consulta clima por nombre de ciudad.GET/api/weather?lat={lat}&lon={lon}Consulta clima por coordenadas del mapa.POST/api/favorites/addAgrega la ciudad actual a los favoritos del usuario.
📄 LicenciaEste proyecto está bajo la licencia MIT. Libre para uso, modificación y distribución.
