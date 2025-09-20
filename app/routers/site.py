# app/routers/site.py
import os
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import get_db
from ..models import Visitante, User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper: lista imagens em app/static/images (jpg/png/gif)
def _listar_imagens():
    imagens = []
    base = os.path.join("app", "static", "images")
    if os.path.isdir(base):
        for fname in sorted(os.listdir(base)):
            if fname.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
                imagens.append(f"/static/images/{fname}")
    return imagens

@router.get("/fotos", response_class=HTMLResponse)
def fotos(request: Request):
    imagens = _listar_imagens()
    return request.app.state.templates.TemplateResponse("fotos.html", {"request": request, "imagens": imagens})

@router.get("/contato", response_class=HTMLResponse)
def contato_get(request: Request, db: Session = Depends(get_db)):
    visitantes = db.query(Visitante).order_by(Visitante.id.desc()).all()
    return request.app.state.templates.TemplateResponse("contato.html", {"request": request, "visitantes": visitantes})

@router.post("/contato")
def contato_post(request: Request, nome: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    novo = Visitante(nome=nome.strip(), email=email.strip())
    db.add(novo)
    db.commit()
    # redirect com 303 para evitar reenvio de formulário ao atualizar
    return RedirectResponse(url="/contato", status_code=303)

# Registro de usuário simples (persistência no mesmo model User já existente)
@router.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    msg = request.query_params.get("msg")
    return request.app.state.templates.TemplateResponse("register.html", {"request": request, "msg": msg})

@router.post("/register")
def register_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    username = username.strip()
    if not username or not password:
        return RedirectResponse(url="/register?msg=Preencha+usuário+e+senha", status_code=303)
    existent = db.query(User).filter(User.username == username).first()
    if existent:
        return RedirectResponse(url="/register?msg=Usuário+já+existe", status_code=303)
    hashed = pwd_context.hash(password)
    novo = User(username=username, hashed_password=hashed)
    db.add(novo)
    db.commit()
    return RedirectResponse(url="/register?msg=Registrado+com+sucesso", status_code=303)
