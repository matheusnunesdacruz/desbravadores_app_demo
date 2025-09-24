import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from datetime import datetime

from .database import Base, engine
from .routers import core
from app import auth  # mantém o módulo de autenticação existente
from app.routers import site  # novo router site

def create_app() -> FastAPI:
    app = FastAPI(
        title="Clube de Desbravadores Monte das Oliveiras",
        version="1.0.0"
    )

    # CORS (configuração permissiva; ajuste para produção)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Cria as tabelas (SQLite/Postgres conforme DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    # Static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Templates (HTML)
    templates = Jinja2Templates(directory="app/templates")
    # Expor helper 'now' para os templates (usa datetime.utcnow)
    templates.env.globals["now"] = datetime.utcnow
    app.state.templates = templates

    # Inclui os routers
    app.include_router(core.router)
    
    # Login/Register disponíveis em /auth/login e também /login
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(auth.router)  

    app.include_router(site.router, tags=["site"])

    return app

# Cria a aplicação
app = create_app()
