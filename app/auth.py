from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Role
from fastapi.templating import Jinja2Templates

SECRET_KEY = "minha_chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


# ====================
# UTILITÁRIOS
# ====================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# ====================
# ROTAS DE LOGIN
# ====================
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuário ou senha incorretos"},
            status_code=401,
        )

    # grava na sessão
    request.session["user"] = {
        "id": user.id,
        "username": user.username,
        "role": user.role if isinstance(user.role, str) else user.role.value,
    }
    return RedirectResponse(url="/", status_code=303)


# ====================
# REGISTRO
# ====================
@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Nome de usuário já cadastrado"},
            status_code=400,
        )

    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password, role=Role.USER)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # login automático após registro
    request.session["user"] = {
        "id": new_user.id,
        "username": new_user.username,
        "role": new_user.role if isinstance(new_user.role, str) else new_user.role.value,
    }
    return RedirectResponse(url="/", status_code=303)


# ====================
# LOGOUT
# ====================
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
