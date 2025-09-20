from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.routers import core, site

app = FastAPI()

# Configurar arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates (Jinja2)
templates = Jinja2Templates(directory="app/templates")

# Incluir rotas existentes
app.include_router(core.router)
app.include_router(site.router)

# Rotas principais
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/contato", response_class=HTMLResponse)
async def contato(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@app.get("/fotos", response_class=HTMLResponse)
async def fotos(request: Request):
    return templates.TemplateResponse("fotos.html", {"request": request})

@app.get("/usuarios", response_class=HTMLResponse)
async def usuarios(request: Request):
    # ⚠️ Aqui você pode depois conectar com o banco (User model)
    return templates.TemplateResponse("desbravadores.html", {"request": request})

# Alias para evitar erro de cache/style.css errado
@app.get("/static/style.css")
async def style_alias():
    return FileResponse(os.path.join("app", "static", "styles.css"))
