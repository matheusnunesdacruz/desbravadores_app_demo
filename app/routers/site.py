from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
import os, shutil
from typing import List

from ..database import get_db
from ..models import GuestbookEntry  # novo modelo
from .. import models

router = APIRouter()

# Pasta onde ficam as imagens
UPLOAD_DIR = os.path.join("app", "static", "images")


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
    imgs = []
    if os.path.isdir(UPLOAD_DIR):
        for fn in os.listdir(UPLOAD_DIR):
            if fn.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
                imgs.append("/static/images/" + fn)
    return request.app.state.templates.TemplateResponse("fotos.html", {"request": request, "images": imgs})


# Novo endpoint: upload de foto
@router.post("/fotos/upload")
async def upload_foto(file: UploadFile = File(...)):
    """
    Faz upload de uma imagem e salva em static/images
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # garante que a pasta existe
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return RedirectResponse(url="/fotos", status_code=303)


# Novo endpoint: excluir foto
@router.post("/fotos/delete")
async def delete_foto(filename: str = Form(...)):
    """
    Exclui uma imagem do diretório static/images
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return RedirectResponse(url="/fotos", status_code=303)


@router.get("/contato", response_class=HTMLResponse)
def contato(request: Request, db: Session = Depends(get_db)):
    """
    Página de contato / livro de visitas (lista entradas)
    """
    entries: List[GuestbookEntry] = (
        db.query(GuestbookEntry)
        .order_by(GuestbookEntry.created_at.desc())
        .limit(100)
        .all()
    )
    return request.app.state.templates.TemplateResponse(
        "contato.html", {"request": request, "entries": entries}
    )


@router.post("/contato")
def contato_post(
    request: Request,
    nome: str = Form(...),
    email: str = Form(None),
    mensagem: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Salva uma nova mensagem no livro de visitas
    """
    entry = GuestbookEntry(nome=nome, email=email, mensagem=mensagem)
    db.add(entry)
    db.commit()
    return RedirectResponse(url="/contato", status_code=303)
