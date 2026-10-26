# ♡ Cine Divas ♡

Site em Flask com **10 filmes de romance**, cadastro e login de usuárias, num visual bem **anos 2000** (rosa e prata, brega com orgulho ✧).

## Funcionalidades
- **Cadastro** com nome, e-mail e senha (o e-mail é o login)
- **Login** com link "Você tem cadastro?" levando para o cadastro
- **CRUD de filmes**: cadastrar, listar (com busca), ver detalhe, editar e excluir
- Usuárias e filmes salvos em **SQLite** (`instance/cine_divas.db`), senha sempre **hasheada**
- Acesso ao banco com `sqlite3` puro (sem ORM), concentrado na classe `Filme` (`app/models/filme.py`)

## Requisitos
- Python 3.10 ou superior

## Como executar (Windows)

1. Abra o terminal na pasta do projeto.
2. Crie o ambiente virtual (só na primeira vez):
   ```bash
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - PowerShell: `venv\Scripts\Activate.ps1`
   - CMD: `venv\Scripts\activate.bat`
   - Git Bash: `source venv/Scripts/activate`
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Rode o servidor:
   ```bash
   python run.py
   ```
6. Acesse **http://127.0.0.1:5000** no navegador.

Na primeira vez, clique em **"Não? Clique aqui e cadastre-se"**, crie sua conta e depois faça login.

> No Linux/macOS, troque o passo 3 por `source venv/bin/activate`.

## Estrutura
```
run.py                 # inicia o servidor
app/                   # código Python (app factory, banco, controllers)
app/models/filme.py    # classe Filme: todo o SQL da tabela filmes
views/                 # páginas HTML (Jinja)
static/css/style.css   # estilo Y2K
static/img/            # pôsteres dos filmes
instance/              # banco SQLite (criado automaticamente)
```

## Créditos das imagens
Os pôsteres pertencem aos respectivos estúdios/distribuidoras e foram obtidos da Wikipédia (en) e do
[TMDB](https://www.themoviedb.org/) (*Nos Vemos em Vênus*). Uso apenas educacional, sem fins comerciais.

## Dicas
- **O CSS não aparece?** Dê Ctrl+F5 no navegador para limpar o cache.
- **Zerar o banco:** pare o servidor e apague o arquivo `instance/cine_divas.db`. Ao subir de novo, as tabelas são
  recriadas e os 10 filmes iniciais voltam (as contas são apagadas).
- **Produção:** defina a variável de ambiente `SECRET_KEY` com um valor secreto.
