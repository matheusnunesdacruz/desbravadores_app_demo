import os
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from .database import Base, engine

# routers (importa com try/except para evitar erro caso algum router esteja faltando)
try:
    from .routers import core, site
except Exception:
    core = None
    site = None

try:
    from . import auth
except Exception:
    auth = None


def create_app() -> FastAPI:
    app = FastAPI(
        title="Clube de Desbravadores Monte das Oliveiras",
        version="1.0.0"
    )

    # Session (use uma variável de ambiente em produção)
    try:
        from starlette.middleware.sessions import SessionMiddleware
        secret = os.getenv("SESSION_SECRET", "uma_chave_segura_de_sessao")
        app.add_middleware(SessionMiddleware, secret_key=secret)
    except ModuleNotFoundError:
        # Evita quebrar o app se faltar itsdangerous
        print("⚠️ SessionMiddleware não carregado (instale itsdangerous).")

    # CORS (ajuste em produção)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Paths relativos ao pacote
    pkg_dir = Path(__file__).resolve().parent

    # Static files
    static_dir = pkg_dir / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Templates Jinja2
    templates = Jinja2Templates(directory=str(pkg_dir / "templates"))
    templates.env.globals["datetime"] = datetime
    app.state.templates = templates

    # Cria tabelas se necessário (SQLite / Postgres conforme DATABASE_URL)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        # ignore em ambientes onde não queremos criar automaticamente
        pass

    # Incluir routers (com checagem)
    if core is not None and getattr(core, "router", None) is not None:
        app.include_router(core.router)

    if auth is not None and getattr(auth, "router", None) is not None:
        # registra auth somente com prefix (evita rotas duplicadas)
        app.include_router(auth.router, prefix="/auth", tags=["auth"])

    if site is not None and getattr(site, "router", None) is not None:
        app.include_router(site.router, tags=["site"])

    return app


# app exportado para uvicorn: uvicorn app.main:app --reload
app = create_app()
