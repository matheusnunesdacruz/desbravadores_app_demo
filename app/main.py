from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Configuração de templates
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

# Montar static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Alias para corrigir /static/style.css
@app.get("/static/style.css")
async def style_alias():
    return FileResponse(os.path.join("app", "static", "styles.css"))

# Importa routers
from app.routers import core, fotos, contato, usuarios
app.include_router(core.router)
app.include_router(fotos.router)
app.include_router(contato.router)
app.include_router(usuarios.router)
