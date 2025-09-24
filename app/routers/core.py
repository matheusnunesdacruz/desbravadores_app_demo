from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from datetime import date
from ..database import get_db
from ..models import Unidade, Classe, Especialidade, Desbravador, Caixa, Mensalidade, Patrimonio, Ata, Ato, TipoLancamento
from ..utils import parse_date
from typing import Optional

router = APIRouter()

# ---------- Home & Dashboard ----------
@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    total_desbravadores = db.query(Desbravador).count()
    saldo = 0.0
    for l in db.query(Caixa).all():
        saldo += l.valor if l.tipo == TipoLancamento.ENTRADA else -l.valor
    em_atraso = db.query(Mensalidade).filter(Mensalidade.pago == False).count()
    return request.app.state.templates.TemplateResponse("home.html", {
        "request": request,
        "total_desbravadores": total_desbravadores,
        "saldo": saldo,
        "em_atraso": em_atraso,
    })

# ---------- Cadastros ----------
@router.get("/unidades", response_class=HTMLResponse)
def unidades_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Unidade).all()
    return request.app.state.templates.TemplateResponse("unidades.html", {"request": request, "data": data})

@router.post("/unidades")
def unidades_add(nome: str = Form(...), descricao: str = Form(""), db: Session = Depends(get_db)):
    db.add(Unidade(nome=nome, descricao=descricao)); db.commit()
    return RedirectResponse("/unidades", status_code=303)

@router.post("/unidades/{id}/delete")
def unidades_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Unidade, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/unidades", status_code=303)

@router.get("/classes", response_class=HTMLResponse)
def classes_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Classe).all()
    return request.app.state.templates.TemplateResponse("classes.html", {"request": request, "data": data})

@router.post("/classes")
def classes_add(nome: str = Form(...), nivel: int = Form(1), db: Session = Depends(get_db)):
    db.add(Classe(nome=nome, nivel=nivel)); db.commit()
    return RedirectResponse("/classes", status_code=303)

@router.post("/classes/{id}/delete")
def classes_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Classe, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/classes", status_code=303)

@router.get("/especialidades", response_class=HTMLResponse)
def esp_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Especialidade).all()
    return request.app.state.templates.TemplateResponse("especialidades.html", {"request": request, "data": data})

@router.post("/especialidades")
def esp_add(nome: str = Form(...), area: str = Form("Geral"), db: Session = Depends(get_db)):
    db.add(Especialidade(nome=nome, area=area)); db.commit()
    return RedirectResponse("/especialidades", status_code=303)

@router.post("/especialidades/{id}/delete")
def esp_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Especialidade, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/especialidades", status_code=303)

@router.get("/desbravadores", response_class=HTMLResponse)
def desbravadores_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Desbravador).all()
    unidades = db.query(Unidade).all()
    classes = db.query(Classe).all()
    especialidades = db.query(Especialidade).all()
    return request.app.state.templates.TemplateResponse("desbravadores.html", {
        "request": request, "data": data, "unidades": unidades, "classes": classes, "especialidades": especialidades
    })

@router.post("/desbravadores")
def desbravadores_add(
    nome: str = Form(...),
    data_nascimento: str = Form(None),
    unidade_id: int | None = Form(None),
    classe_id: int | None = Form(None),
    responsavel: str = Form(""),
    telefone_responsavel: str = Form(""),
    documento: str = Form(""),
    db: Session = Depends(get_db),
):
    obj = Desbravador(
        nome=nome,
        data_nascimento=parse_date(data_nascimento),
        unidade_id=unidade_id if unidade_id else None,
        classe_id=classe_id if classe_id else None,
        responsavel=responsavel,
        telefone_responsavel=telefone_responsavel,
        documento=documento,
    )
    db.add(obj); db.commit()
    return RedirectResponse("/desbravadores", status_code=303)

@router.post("/desbravadores/{id}/delete")
def desbravadores_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Desbravador, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/desbravadores", status_code=303)

# ---------- Mensalidades ----------
@router.get("/mensalidades", response_class=HTMLResponse)
def mensalidades_list(request: Request, db: Session = Depends(get_db)):
    des = db.query(Desbravador).all()
    data = db.query(Mensalidade).all()
    return request.app.state.templates.TemplateResponse("mensalidades.html", {"request": request, "data": data, "des": des})

@router.post("/mensalidades")
def mensalidades_add(desbravador_id: int = Form(...), competencia: str = Form(...), valor: float = Form(...), pago: bool = Form(False), data_pagamento: str = Form(None), db: Session = Depends(get_db)):
    obj = Mensalidade(
        desbravador_id=desbravador_id, competencia=competencia, valor=valor,
        pago=pago, data_pagamento=parse_date(data_pagamento)
    )
    db.add(obj); db.commit()
    return RedirectResponse("/mensalidades", status_code=303)

@router.post("/mensalidades/{id}/toggle")
def mensalidade_toggle(id: int, db: Session = Depends(get_db)):
    m = db.get(Mensalidade, id)
    if m:
        m.pago = not m.pago
        db.commit()
    return RedirectResponse("/mensalidades", status_code=303)

@router.post("/mensalidades/{id}/delete")
def mensalidades_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Mensalidade, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/mensalidades", status_code=303)

# ---------- Caixa / Custos ----------
@router.get("/caixa", response_class=HTMLResponse)
def caixa_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Caixa).order_by(Caixa.data.desc()).all()
    saldo = 0.0
    for l in data:
        saldo += l.valor if l.tipo == TipoLancamento.ENTRADA else -l.valor
    return request.app.state.templates.TemplateResponse("caixa.html", {"request": request, "data": data, "saldo": saldo})

@router.post("/caixa")
def caixa_add(data: str = Form(...), tipo: str = Form(...), categoria: str = Form("Geral"), descricao: str = Form(""), valor: float = Form(...), db: Session = Depends(get_db)):
    obj = Caixa(data=parse_date(data), tipo=tipo, categoria=categoria, descricao=descricao, valor=valor)
    db.add(obj); db.commit()
    return RedirectResponse("/caixa", status_code=303)

@router.post("/caixa/{id}/delete")
def caixa_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Caixa, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/caixa", status_code=303)

# ---------- Patrimônio ----------
@router.get("/patrimonio", response_class=HTMLResponse)
def patrimonio_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Patrimonio).all()
    return request.app.state.templates.TemplateResponse("patrimonio.html", {"request": request, "data": data})

@router.post("/patrimonio")
def patrimonio_add(nome: str = Form(...), descricao: str = Form(""), data_aquisicao: str = Form(None), valor: float = Form(0.0), status: str = Form("Em uso"), db: Session = Depends(get_db)):
    obj = Patrimonio(nome=nome, descricao=descricao, data_aquisicao=parse_date(data_aquisicao), valor=valor, status=status)
    db.add(obj); db.commit()
    return RedirectResponse("/patrimonio", status_code=303)

@router.post("/patrimonio/{id}/delete")
def patrimonio_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Patrimonio, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/patrimonio", status_code=303)

# ---------- Atas & Atos ----------
@router.get("/atas", response_class=HTMLResponse)
def atas_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Ata).order_by(Ata.data.desc()).all()
    return request.app.state.templates.TemplateResponse("atas.html", {"request": request, "data": data})

@router.post("/atas")
def atas_add(data: str = Form(...), titulo: str = Form(...), conteudo: str = Form(...), db: Session = Depends(get_db)):
    db.add(Ata(data=parse_date(data), titulo=titulo, conteudo=conteudo)); db.commit()
    return RedirectResponse("/atas", status_code=303)

@router.post("/atas/{id}/delete")
def atas_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Ata, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/atas", status_code=303)

@router.get("/atos", response_class=HTMLResponse)
def atos_list(request: Request, db: Session = Depends(get_db)):
    data = db.query(Ato).order_by(Ato.data.desc()).all()
    return request.app.state.templates.TemplateResponse("atos.html", {"request": request, "data": data})

@router.post("/atos")
def atos_add(data: str = Form(...), titulo: str = Form(...), conteudo: str = Form(...), db: Session = Depends(get_db)):
    db.add(Ato(data=parse_date(data), titulo=titulo, conteudo=conteudo)); db.commit()
    return RedirectResponse("/atos", status_code=303)

@router.post("/atos/{id}/delete")
def atos_delete(id: int, db: Session = Depends(get_db)):
    obj = db.get(Ato, id); 
    if obj: db.delete(obj); db.commit()
    return RedirectResponse("/atos", status_code=303)

# ---------- Relatórios ----------
@router.get("/relatorios/fluxo-caixa", response_class=HTMLResponse)
def rel_fluxo_caixa(request: Request, db: Session = Depends(get_db)):
    entradas = sum(l.valor for l in db.query(Caixa).filter(Caixa.tipo == "ENTRADA").all())
    saidas = sum(l.valor for l in db.query(Caixa).filter(Caixa.tipo == "SAIDA").all())
    saldo = entradas - saidas
    return request.app.state.templates.TemplateResponse("rel_fluxo_caixa.html", {"request": request, "entradas": entradas, "saidas": saidas, "saldo": saldo})

@router.get("/relatorios/patrimonio", response_class=HTMLResponse)
def rel_patrimonio(request: Request, db: Session = Depends(get_db)):
    itens = db.query(Patrimonio).all()
    total = sum(i.valor for i in itens)
    return request.app.state.templates.TemplateResponse("rel_patrimonio.html", {"request": request, "itens": itens, "total": total})

@router.get("/relatorios/livro-ata-atos", response_class=HTMLResponse)
def rel_livro_ata_atos(request: Request, db: Session = Depends(get_db)):
    atas = db.query(Ata).order_by(Ata.data).all()
    atos = db.query(Ato).order_by(Ato.data).all()
    return request.app.state.templates.TemplateResponse("rel_livro_ata_atos.html", {"request": request, "atas": atas, "atos": atos})

@router.get("/relatorios/mensalidade", response_class=HTMLResponse)
def rel_mensalidade(request: Request, db: Session = Depends(get_db)):
    pendentes = db.query(Mensalidade).filter(Mensalidade.pago == False).all()
    pagos = db.query(Mensalidade).filter(Mensalidade.pago == True).all()
    return request.app.state.templates.TemplateResponse("rel_mensalidade.html", {"request": request, "pendentes": pendentes, "pagos": pagos})

@router.get("/relatorios/unidades-classes-especialidades-desbravadores", response_class=HTMLResponse)
def rel_uceds(request: Request, db: Session = Depends(get_db)):
    unidades = db.query(Unidade).all()
    classes = db.query(Classe).all()
    especialidades = db.query(Especialidade).all()
    des = db.query(Desbravador).all()
    return request.app.state.templates.TemplateResponse("rel_uceds.html", {"request": request, "unidades": unidades, "classes": classes, "especialidades": especialidades, "des": des})

@router.get("/relatorios/autorizacao-saida", response_class=HTMLResponse)
def rel_autorizacao_saida(
    request: Request,
    desbravador_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    d = None
    if desbravador_id is not None:
        d = db.get(Desbravador, desbravador_id)
    return request.app.state.templates.TemplateResponse(
        "rel_autorizacao_saida.html",
        {"request": request, "d": d}
    )
