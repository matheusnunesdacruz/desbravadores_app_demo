from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.main import templates
from ..database import get_db
from ..models import User

router = APIRouter()

@router.get("/usuarios", response_class=HTMLResponse)
def usuarios_list(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(User).order_by(User.id.desc()).all()
    return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})

@router.post("/usuarios/{user_id}/delete")
def usuarios_delete(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse("/usuarios", status_code=303)
