from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import core, site

app = FastAPI()

# Configurar arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Incluir rotas existentes
app.include_router(core.router)
app.include_router(site.router)

# Rotas principais do site
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
    # ⚠️ Ajustar para buscar usuários no banco se já tiver model
    return templates.TemplateResponse("desbravadores.html", {"request": request})
