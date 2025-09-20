import os
import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.main import templates
from ..database import get_db
from ..models import Visitante

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONTATOS_FILE = DATA_DIR / "contatos.json"

def _load_messages():
    if not CONTATOS_FILE.exists():
        return []
    try:
        return json.loads(CONTATOS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def _save_message(entry: dict):
    msgs = _load_messages()
    msgs.insert(0, entry)  # insere no início (mais recente primeiro)
    CONTATOS_FILE.write_text(json.dumps(msgs, ensure_ascii=False, indent=2), encoding="utf-8")

@router.get("/contato", response_class=HTMLResponse)
def contato_form(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@router.post("/contato")
def contato_submit(nome: str = Form(...), email: str = Form(...), mensagem: str = Form(""), db: Session = Depends(get_db)):
    # Cria um visitante (se quiser manter histórico simples no DB)
    v = Visitante(nome=nome, email=email)
    db.add(v)
    db.commit()

    # Salva a mensagem em JSON (não altera o modelo DB existente)
    entry = {
        "nome": nome,
        "email": email,
        "mensagem": mensagem,
        "criado_em": datetime.utcnow().isoformat()
    }
    _save_message(entry)

    return RedirectResponse("/contato?msg=Enviado+com+sucesso", status_code=303)

@router.get("/contato/lista", response_class=HTMLResponse)
def contato_lista(request: Request, db: Session = Depends(get_db)):
    visitantes = db.query(Visitante).order_by(Visitante.criado_em.desc()).all()
    messages = _load_messages()
    # messages is a list of dicts; pass to template
    return templates.TemplateResponse("contato_lista.html", {"request": request, "visitantes": visitantes, "messages": messages})
