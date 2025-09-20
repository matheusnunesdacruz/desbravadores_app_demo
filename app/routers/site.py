from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.main import templates
from ..database import get_db
from ..models import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

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

@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    msg = request.query_params.get("msg")
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

@router.post("/login")
def login_post(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return RedirectResponse(url="/login?msg=Credenciais+inválidas", status_code=303)
    # NOTA: não implementei sessão/cookie aqui (simplificação).
    return RedirectResponse(url="/?msg=Login+ok", status_code=303)
