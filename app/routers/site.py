from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
import os
from typing import List

from ..database import get_db
from ..models import GuestbookEntry  # novo modelo
from .. import models

router = APIRouter()

@router.get("/boas-vindas", response_class=HTMLResponse)
def boas_vindas(request: Request):
    """
    Página de boas-vindas — explica a razão do site e mostra uma imagem.
    """
    return request.app.state.templates.TemplateResponse("welcome.html", {"request": request})

@router.get("/fotos", response_class=HTMLResponse)
def fotos(request: Request):
    """
    Mostra todas as fotos da pasta static/images
    """
    images_dir = os.path.join("app", "static", "images")
    imgs = []
    if os.path.isdir(images_dir):
        for fn in os.listdir(images_dir):
            if fn.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                imgs.append("/static/images/" + fn)
    return request.app.state.templates.TemplateResponse("fotos.html", {"request": request, "images": imgs})

@router.get("/contato", response_class=HTMLResponse)
def contato(request: Request, db: Session = Depends(get_db)):
    """
    Página de contato / livro de visitas (lista entradas)
    """
    entries: List[GuestbookEntry] = db.query(GuestbookEntry).order_by(GuestbookEntry.created_at.desc()).limit(100).all()
    return request.app.state.templates.TemplateResponse("contato.html", {"request": request, "entries": entries})

@router.post("/contato")
def contato_post(request: Request, nome: str = Form(...), email: str = Form(None), mensagem: str = Form(...), db: Session = Depends(get_db)):
    entry = GuestbookEntry(nome=nome, email=email, mensagem=mensagem)
    db.add(entry)
    db.commit()
    return RedirectResponse(url="/contato", status_code=303)
