from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
import httpx

from database import engine, Base, get_db
import models
import auth

# Crear tablas en SQLite al arrancar el servidor
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GeoWeather SaaS")

# Middleware para sesiones cifradas en Cookies
app.add_middleware(SessionMiddleware, secret_key="geoweather_super_secret_key_2026")

templates = Jinja2Templates(directory="templates")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Obtiene el usuario autenticado actualmente desde la sesión"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(models.User).filter(models.User.id == user_id).first()


# ==========================================
# RUTAS DE AUTENTICACIÓN Y NAVEGACIÓN
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Cargar lugares favoritos guardados por el usuario
    favoritos = db.query(models.FavoriteLocation).filter(
        models.FavoriteLocation.user_id == user.id
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"user": user, "favoritos": favoritos}
    )

@app.get("/register", response_class=HTMLResponse)
async def show_register(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"error": None})

@app.post("/register", response_class=HTMLResponse)
async def do_register(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Verificar si el correo ya existe
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={"error": "Este correo electrónico ya está registrado."}
        )

    # Crear nuevo usuario con contraseña cifrada
    new_user = models.User(
        nombre=nombre,
        email=email,
        password_hash=auth.hash_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Iniciar sesión automáticamente tras el registro
    request.session["user_id"] = new_user.id
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login", response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})

@app.post("/login", response_class=HTMLResponse)
async def do_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Credenciales inválidas. Por favor intenta de nuevo."}
        )

    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


# ==========================================
# API DE CLIMA Y GEOLOCALIZACIÓN
# ==========================================

@app.get("/api/weather")
async def get_weather(ciudad: str = None, lat: float = None, lon: float = None):
    """
    Obtiene coordenadas de la ciudad por nombre O resuelve el lugar mediante
    coordenadas (lat, lon) al hacer clic en el mapa, y consulta Open-Meteo.
    """
    async with httpx.AsyncClient(verify=False) as client:
        # Opción 1: Consulta por nombre de ciudad (Buscador)
        if ciudad:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es&format=json"
            geo_res = await client.get(geo_url, timeout=5.0)
            
            if geo_res.status_code != 200 or not geo_res.json().get("results"):
                return JSONResponse(status_code=404, content={"error": "Ciudad no encontrada"})

            geo_data = geo_res.json()["results"][0]
            lat = geo_data["latitude"]
            lon = geo_data["longitude"]
            nombre = geo_data["name"]
            pais = geo_data.get("country", "")

        # Opción 2: Consulta por coordenadas lat/lon (Clic en el mapa)
        elif lat is not None and lon is not None:
            rev_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
            rev_res = await client.get(rev_url, headers={"User-Agent": "GeoWeatherSaaSApp/1.0"}, timeout=5.0)
            
            nombre = "Ubicación Seleccionada"
            pais = ""
            
            if rev_res.status_code == 200:
                addr = rev_res.json().get("address", {})
                nombre = (
                    addr.get("city") or 
                    addr.get("town") or 
                    addr.get("village") or 
                    addr.get("county") or 
                    addr.get("state") or 
                    "Ubicación Seleccionada"
                )
                pais = addr.get("country", "")
        else:
            return JSONResponse(status_code=400, content={"error": "Debes proporcionar una ciudad o coordenadas (lat, lon)"})

        # Consulta de clima actual con Open-Meteo API
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&"
            f"timezone=auto"
        )
        weather_res = await client.get(weather_url, timeout=5.0)
        
        if weather_res.status_code != 200:
            return JSONResponse(status_code=500, content={"error": "Error al consultar el servicio de clima"})

        weather_data = weather_res.json()["current"]

        return {
            "ciudad": nombre,
            "pais": pais,
            "latitud": lat,
            "longitud": lon,
            "temperatura": weather_data["temperature_2m"],
            "sensacion": weather_data["apparent_temperature"],
            "humedad": weather_data["relative_humidity_2m"],
            "viento": weather_data["wind_speed_10m"],
            "weather_code": weather_data["weather_code"]
        }


# ==========================================
# GESTIÓN DE FAVORITOS
# ==========================================

@app.post("/api/favorites/add")
async def add_favorite(
    request: Request,
    ciudad: str = Form(...),
    pais: str = Form(""),
    lat: float = Form(...),
    lon: float = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse(status_code=401, content={"error": "No autorizado"})

    # Evitar duplicados
    exist = db.query(models.FavoriteLocation).filter(
        models.FavoriteLocation.user_id == user.id,
        models.FavoriteLocation.nombre_ciudad == ciudad
    ).first()

    if not exist:
        fav = models.FavoriteLocation(
            nombre_ciudad=ciudad,
            pais=pais,
            latitud=lat,
            longitud=lon,
            user_id=user.id
        )
        db.add(fav)
        db.commit()

    return {"status": "ok"}