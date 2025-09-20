from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# --- Jinja2 helpers: add a `date` filter and `now()` global for templates ---
from datetime import datetime as _datetime

def _date_filter(value, fmt="%Y"):
    """Formats datetime-like values. Accepts:
       - a datetime/date object (uses .strftime(fmt))
       - the literal string 'now' (returns current datetime formatted)
       - otherwise returns str(value)
    """
    try:
        if isinstance(value, str) and value.lower() == "now":
            return _datetime.now().strftime(fmt)
        return value.strftime(fmt)
    except Exception:
        return str(value)

# register filter
templates.env.filters['date'] = _date_filter

# helper to get current datetime when rendering: use `{{ now() | date("%Y") }}`
templates.env.globals['now'] = lambda: _datetime.now()
# ---------------------------------------------------------------

# IMPORTS DE ROTAS
from app.routers import core

app.include_router(core.router)
