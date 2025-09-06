# Sistema de Gerenciamento de Clube de Desbravadores (FastAPI + PostgreSQL)

Pronto para deploy no **Render.com**. Inclui:
- Cadastro de Unidades, Classes, Especialidades e Desbravadores
- Controle de Mensalidade
- Controle de Caixa (entradas/saídas) e de Custos
- Controle de Patrimônio
- Controle de Atas e Atos
- Relatórios: autorização de saída, fluxo de caixa, patrimônio, Livro Ata/Atos, mensalidade, unidade/classes/especialidades/desbravadores
- UI simples com Jinja2 (sem autenticação por simplicidade)
- Banco: PostgreSQL (Render) com fallback local em SQLite

## Estrutura
```
app/
  main.py
  database.py
  models.py
  utils.py
  routers/
  templates/
  static/
render.yaml
requirements.txt
```
## Rodando localmente
1. Python 3.10+
2. `python -m venv .venv && source .venv/bin/activate` (Linux/Mac) ou `.\.venv\Scriptsctivate` (Windows)
3. `pip install -r requirements.txt`
4. (Opcional) Defina `DATABASE_URL` para seu Postgres. Caso não, usa SQLite local.
5. `uvicorn app.main:app --reload`
6. Acesse http://localhost:8000

## Deploy no Render
1. Faça fork/commit deste repositório no GitHub.
2. Em **Render > New > Web Service**, conecte ao repo.
3. Ambiente: Python 3.10+
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn -k uvicorn.workers.UvicornWorker app.main:app`
6. Configure env vars:
   - `DATABASE_URL` (fornecido pelo Render Postgres ou outro provedor). Exemplos:
     - `postgres://USER:PASSWORD@HOST:PORT/DB` (Render)
     - Nós convertemos automaticamente para `postgresql+psycopg2://...`
   - (Opcional) `SECRET_KEY` para sessões/CSRF simples.
7. Primeiro start criará as tabelas automaticamente.

## Migrações
Para simplicidade, as tabelas são criadas automaticamente no startup. Em produção de longo prazo, recomende-se Alembic.

## Credenciais / Segurança
Este exemplo **não possui autenticação**. Para uso real, adicione login/controle de acesso antes de dados reais.
