# ♡ Cine Divas ♡

Aplicação web MPA em **Flask + Jinja2 + SQLite3** para guardar e avaliar **filmes de romance**, num visual bem
**anos 2000** (rosa e prata, brega com orgulho ✧). Projeto final de Laboratório de Programação 1 (SPOLBP1).

## Funcionalidades
- **Usuárias:** cadastro, login e logout. Senha sempre com hash (`werkzeug.security`).
- **Filmes:** cadastrar, listar (com busca por título), ver detalhe, editar e excluir.
- **Avaliações:** dar nota (1 a 5) e comentário a um filme, listar as minhas avaliações e excluir.
- Cada usuária só vê e mexe nos **próprios** filmes e avaliações (`WHERE usuario_id = ?`).
- Middleware `@login_required` (valida a usuária no banco e guarda em `g.usuario`).
- **Cookie** que lembra o último e-mail usado no login (30 dias).
- Flash messages por categoria, página **404** personalizada e **logs** (`app.logger`).

## 🔑 Usuária de teste
Criada pelo `iniciar_bd.py`, já com os 10 filmes iniciais:

| E-mail | Senha |
|---|---|
| `diva@cinedivas.com` | `diva123` |

## Como executar

1. Crie e ative o ambiente virtual (só na primeira vez):
   ```bash
   python -m venv venv
   ```
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Crie o banco (tabelas + usuária de teste + 10 filmes). Pode rodar de novo sem duplicar nada:
   ```bash
   python iniciar_bd.py
   ```
4. Rode o servidor e acesse **http://127.0.0.1:5000**:
   ```bash
   python run.py
   ```

## Estrutura (MVC)
```
iniciar_bd.py               # cria as tabelas (CREATE TABLE) e os dados iniciais
banco_sistema.db            # banco SQLite (gerado pelo iniciar_bd.py)
run.py                      # inicia o servidor Flask
app/
  __init__.py               # create_app: secret_key, blueprints, erro 404 e logger
  db.py                     # classe DatabaseConnection (__enter__ e __exit__)
  models/                   # Usuario, Filme, Avaliacao (todo o SQL fica aqui)
  controllers/              # blueprints auth_bp, filmes_bp, avaliacoes_bp (sem SQL)
  utils/auth_middleware.py  # decorator @login_required
  views/                    # templates Jinja2 (herdam de base.html)
  static/                   # CSS e pôsteres
tests/test_app.py           # testes automáticos
```

## Testes
```bash
python -m unittest -v
```
Os testes usam um banco temporário, então o `banco_sistema.db` não é alterado.

## Dicas
- **Zerar o banco:** apague o `banco_sistema.db` e rode `python iniciar_bd.py` de novo.
- **O CSS não aparece?** Ctrl+F5 no navegador.

## Créditos das imagens
Os pôsteres pertencem aos respectivos estúdios/distribuidoras e foram obtidos da Wikipédia (en) e do
[TMDB](https://www.themoviedb.org/) (*Nos Vemos em Vênus*). Uso apenas educacional, sem fins comerciais.
