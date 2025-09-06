import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .routers import core
from app import auth  # importa o módulo auth

def create_app() -> FastAPI:
    app = FastAPI(
        title="Clube de Desbravadores Monte das Oliveiras",
        version="1.0.0"
    )

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Criação das tabelas no banco
    Base.metadata.create_all(bind=engine)

    # Monta pasta de arquivos estáticos
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Templates (HTML)
    templates = Jinja2Templates(directory="app/templates")
    app.state.templates = templates

    # Inclui os routers
    app.include_router(core.router)
    app.include_router(auth.router, prefix="/auth", tags=["auth"])

    return app

# Cria a aplicação
app = create_app()
