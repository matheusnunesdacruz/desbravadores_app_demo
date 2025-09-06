import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from .database import Base, engine
from .routers import core

def create_app() -> FastAPI:
    app = FastAPI(title="Clube de Desbravadores", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
    )
    Base.metadata.create_all(bind=engine)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    templates = Jinja2Templates(directory="app/templates")
    app.state.templates = templates
    app.include_router(core.router)
    return app

app = create_app()
