from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Base de datos de ejemplo
with open('users.json', 'r') as f:
    users_db = json.load(f)

# Modelo de consulta
class LoginRequest(BaseModel):
    usuario: str
    clave: str

@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/login")
def render_login():
    return FileResponse("./templates/login.html")

@app.post("/login")
async def login(request: LoginRequest):
    # Buscar usuario en la base de datos
    user = next((user for user in users_db if user["usuario"] == request.usuario), None)
    
    if not user:
        # Si el usuario no existe, devolver 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user["clave"] != request.clave:
        # Si la clave es incorrecta, devolver 401
        raise HTTPException(status_code=401, detail="Clave incorrecta")
    
    if user["clave_productiva"] == False:
        # Si la clave es correcta pero la clave_productiva es False, devolver 207
        raise HTTPException(status_code=207, detail="Clave válida pero clave productiva no habilitada")
    
    # Si todo está bien, devolver 200
    return {"message": "Login exitoso"}

@app.get("/dashboard")
def dashboard():
    return FileResponse("./templates/dashboard.html")

@app.exception_handler(StarletteHTTPException)
def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return FileResponse("./templates/loader.html")
