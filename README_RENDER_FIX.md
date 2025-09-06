# Correção de versão do Python no Render

O Render **não lê `runtime.txt`** para Python. Para forçar a versão correta, use **`.python-version`** ou a **env var `PYTHON_VERSION`**.

## O que este patch contém
- `.python-version` com `3.11.9`

## Passo a passo
1. Copie o arquivo `.python-version` para a **raiz do repositório** (no mesmo nível de `requirements.txt`).
2. Faça commit e push:
   ```bash
   git add .python-version
   git commit -m "Fix: forçar Python 3.11.9 no Render (.python-version)"
   git push origin main
   ```
3. No painel do Render (opcional, mas recomendado), em **Environment** adicione:
   - `PYTHON_VERSION=3.11.9`
4. Clique em **Manual Deploy > Clear build cache & deploy** (limpar cache é importante para ele pegar a nova versão).
5. Aguarde o deploy. Nos logs deve aparecer: `Using Python version 3.11.9`.

## Observações
- Mantivemos `psycopg2-binary==2.9.9`. Essa lib é compatível com Python 3.11, então não é necessário trocar.
- Alternativa: migrar para `psycopg[binary]==3.2.3` e ajustar a URL do SQLAlchemy para `postgresql+psycopg://` (não obrigatório).
