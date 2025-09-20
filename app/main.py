from pathlib import Path
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

# --- setup paths robustos (evita problemas se cwd for diferente) ---
BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Desbravadores App")

# Templates (pasta app/templates)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Mount de arquivos estáticos (app/static)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Alias para requests que pedem /static/style.css (compatibilidade)
@app.get("/static/style.css")
async def _style_alias():
    return FileResponse(str(BASE_DIR / "static" / "styles.css"))

# cria as tabelas automaticamente no startup (útil para dev / sqlite)
@app.on_event("startup")
def _create_db_and_tables():
    # importa o módulo database e importa models para registrar metadados
    try:
        from app import models  # garante que as classes ORM sejam importadas
        from app.database import Base, engine
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        # não quebrar startup se algo falhar; loguei via print (Render/ logs mostrarão)
        print("Aviso ao criar tabelas:", e)


# Importar routers **após** templates estarem definidos (evita circular imports)
from app.routers import core, fotos, contato, usuarios, site  # site contém auth/registro
app.include_router(core.router)
app.include_router(fotos.router)
app.include_router(contato.router)
app.include_router(usuarios.router)
app.include_router(site.router)  # site tem register/login (não duplica contato/fotos)
