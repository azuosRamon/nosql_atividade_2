## Como rodar o projeto

1. Clone o repositório e entre na pasta do projeto.
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
3. Ative o ambiente virtual:
   - Windows:
     ```
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source .venv/bin/activate
     ```
4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
5. Copie `.env.example` para `.env` e preencha com sua string do MongoDB Atlas.
6. Rode o servidor:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
7. Acesse [http://localhost:8000](http://localhost:8000) no navegador.