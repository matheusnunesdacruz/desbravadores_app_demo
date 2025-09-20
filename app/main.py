from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os

# Cria o app FastAPI
app = FastAPI()

# Configuração global dos templates
templates = Jinja2Templates(directory="app/templates")

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Alias para corrigir /static/style.css -> /static/styles.css
@app.get("/static/style.css")
async def style_alias():
    return FileResponse(os.path.join("app", "static", "styles.css"))

# Importa e registra routers
from app.routers import core, fotos, contato, usuarios
app.include_router(core.router)
app.include_router(fotos.router)
app.include_router(contato.router)
app.include_router(usuarios.router)
