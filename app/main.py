# app/main.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .routers import core
from .routers import site
from app import auth  # seu módulo auth já existente

def create_app() -> FastAPI:
    app = FastAPI(
        title="Clube de Desbravadores Monte das Oliveiras",
        version="1.0.0"
    )

    # monta arquivos estáticos
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Templates (Jinja2)
    templates = Jinja2Templates(directory="app/templates")
    app.state.templates = templates

    # cria tabelas (apenas para dev/protótipo)
    Base.metadata.create_all(bind=engine)

    # inclui routers
    app.include_router(core.router)
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(site.router)  # novo router para fotos/contato/registro

    return app

# instancia a app
app = create_app()
