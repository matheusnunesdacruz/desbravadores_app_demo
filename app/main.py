from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# --- Jinja2 helpers: add `date`, `format` filters and `now()` global ---
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

def _format_filter(value, fmt="{}"):
    """Aplica Python str.format no valor.
       Ex.: {{ 1234.5 | format("R$ {:.2f}") }} -> 'R$ 1234.50'
    """
    try:
        return fmt.format(value)
    except Exception:
        return str(value)

# registrar filtros
templates.env.filters['date'] = _date_filter
templates.env.filters['format'] = _format_filter

# helper para obter data/hora atual em templates
templates.env.globals['now'] = lambda: _datetime.now()
# ----------------------------------------------------------------------

# IMPORTS DE ROTAS
from app.routers import core

app.include_router(core.router)
