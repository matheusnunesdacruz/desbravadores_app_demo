from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.main import templates

router = APIRouter()

usuarios = []  # Simples armazenamento em memória (pode ser banco no futuro)

@router.get("/usuarios", response_class=HTMLResponse)
def usuarios_list(request: Request):
    return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})

@router.post("/usuarios")
def usuarios_add(nome: str = Form(...), email: str = Form(...)):
    usuarios.append({"nome": nome, "email": email})
    return RedirectResponse("/usuarios", status_code=303)

@router.post("/usuarios/{index}/delete")
def usuarios_delete(index: int):
    if 0 <= index < len(usuarios):
        usuarios.pop(index)
    return RedirectResponse("/usuarios", status_code=303)
