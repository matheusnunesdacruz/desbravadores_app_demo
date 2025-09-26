# Portal de Gerenciamento do Clube de Desbravadores

Este é um sistema web desenvolvido para auxiliar clubes de desbravadores na organização e gerenciamento de suas atividades e validar as especialidades TI. 
O portal permite administrar membros, eventos, patrimônio, mensalidades e interações com visitantes, de forma prática e centralizada.

---

## 🚀 Funcionalidades

- 📋 Cadastro e gerenciamento de membros do clube
- 📅 Registro e acompanhamento de eventos
- 💰 Controle de mensalidades
- 🏠 Gestão de patrimônio
- 💬 Mural de mensagens para visitantes e membros
- 🔑 Sistema de autenticação (login e registro de usuários)

---

## 👥 Documentação de Uso

### Acesso
- O portal pode ser acessado via navegador no endereço publicado (exemplo: `https://desbravadores-app-demo.onrender.com`).
  
### Fluxo principal
1. **Página inicial**: visão geral do clube, informações e brasão.
2. **Área interna**:
   - **Atas**: manter registros oficiais do clube.
   - **Mensalidades**: controle financeiro de contribuições.
   - **Patrimônio**: lista de bens do clube.
   - **Mural**: espaço para mensagens entre membros/visitantes.

### Requisitos do usuário final
- Navegador atualizado (Google Chrome, Firefox, Edge).
- Conexão com a internet.
- Credenciais fornecidas ou cadastro no portal.

---

## ⚙️ Documentação Técnica

### 🛠️ Tecnologias utilizadas
- **Backend**: Python 3.11 + Flask
- **Frontend**: HTML5, CSS3, Bootstrap
- **Banco de Dados**: SQLite (padrão) — pode ser trocado por outro via SQLAlchemy
- **Deploy**: Render

### 📂 Estrutura do projeto
desbravadores_app_demo/
│
├── app/ # Código principal da aplicação Flask
│ ├── routes/ # Rotas (auth, eventos, financeiro, etc.)
│ ├── templates/ # Templates HTML (Jinja2)
│ ├── static/ # Arquivos estáticos (CSS, JS, imagens)
│ └── models.py # Definições do banco de dados
│
├── requirements.txt # Dependências do projeto
├── config.py # Configurações da aplicação
├── run.py # Ponto de entrada da aplicação
└── README.md # Este arquivo

bash
Copiar código

### 📦 Instalação local

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/desbravadores_app_demo.git
cd desbravadores_app_demo
Crie e ative um ambiente virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Inicialize o banco de dados (SQLite por padrão):

bash
Copiar código
flask db init
flask db migrate
flask db upgrade
Rode o servidor local:

bash
Copiar código
flask run
Acesse em: http://127.0.0.1:5000

🌐 Deploy no Render
Faça login no Render.

Crie um novo Web Service e conecte ao repositório do GitHub.

Configure as variáveis de ambiente necessárias:

FLASK_ENV=production

DATABASE_URL (Render gera automaticamente para PostgreSQL)

Defina o comando de start:

bash
Copiar código
gunicorn run:app
Render fará o deploy automático.

🤝 Contribuição
Faça um fork do projeto.

Crie uma branch (git checkout -b feature/minha-feature).

Commit suas alterações (git commit -m 'Adicionei nova feature').

Faça push (git push origin feature/minha-feature).

Abra um Pull Request.

📜 Licença
Este projeto é de uso comunitário para clubes de desbravadores.
Sinta-se livre para adaptar às necessidades do seu clube.

yaml
Copiar código

---

Quer que eu adapte essa documentação para ser **mais formal (como manual técnico institucional)** ou **mais simples (voltada ao usuário final leigo)
