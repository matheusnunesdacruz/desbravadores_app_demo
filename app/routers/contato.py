from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.main import templates

router = APIRouter()

contatos = []  # Armazena mensagens recebidas (pode ser movido para o banco depois)

@router.get("/contato", response_class=HTMLResponse)
def contato_form(request: Request):
    return templates.TemplateResponse("contato.html", {"request": request})

@router.post("/contato")
def contato_submit(nome: str = Form(...), email: str = Form(...), mensagem: str = Form(...)):
    contatos.append({"nome": nome, "email": email, "mensagem": mensagem})
    return RedirectResponse("/contato", status_code=303)

@router.get("/contato/lista", response_class=HTMLResponse)
def contato_lista(request: Request):
    return templates.TemplateResponse("contato_lista.html", {"request": request, "contatos": contatos})
