# 💗 O que foi implementado — Projeto Final Cine Divas

> Alice, este documento explica o que mudou no projeto para cumprir **tudo** o que o PDF do professor pede,
> onde está cada coisa e como justificar no vídeo. Leia com o código aberto do lado.

---

## ⚡ Primeiro: como rodar agora

Mudou uma coisa: **o banco agora é criado por um script**, antes de ligar o site.

```bash
python iniciar_bd.py   # cria o banco, a usuária de teste e os 10 filmes
python run.py          # liga o site em http://127.0.0.1:5000
```

**Login de teste:** `diva@cinedivas.com` / `diva123`

> ⚠️ As contas que existiam antes (no arquivo antigo `instance/cine_divas.db`) **não passam** para o banco novo
> (`banco_sistema.db`). A pasta `instance/` pode ser apagada.

---

## ✅ Checklist do PDF: onde está cada coisa

| Pedido do PDF | Onde está |
|---|---|
| Login, logout e cadastro | `app/controllers/auth_controller.py` |
| Senha com `generate_password_hash` / `check_password_hash` | `auth_controller.py` (cadastro e login) |
| **2 entidades** com cadastro, listagem e exclusão | **Filmes** e **Avaliações** |
| Exclusão por POST validando o dono | rotas `.../excluir` + `WHERE id = ? AND usuario_id = ?` |
| Classe `DatabaseConnection` com `__enter__` e `__exit__` | `app/db.py` |
| `iniciar_bd.py` com `CREATE TABLE`, FK e usuária de teste via `salvar()` | `iniciar_bd.py` (raiz) |
| Models com `with DatabaseConnection() as db:` e SQL com `?` | `app/models/` |
| Filtrar tudo por `usuario_id` | todos os métodos de `Filme` e `Avaliacao` |
| Controllers com Blueprint e **zero SQL** | `app/controllers/` (`auth_bp`, `filmes_bp`, `avaliacoes_bp`) |
| Views com `extends`, `block`, `for`, `if`, `url_for` | `app/views/` |
| `@login_required` em `app/utils/auth_middleware.py` com `@wraps`, validando no banco e usando `g.usuario` | `app/utils/auth_middleware.py` |
| `app.secret_key` | `app/__init__.py` |
| `session.clear()`, `session['user_id']`, `session['username']` | `auth_controller.py` (login e logout) |
| Cookie com `set_cookie` e `request.cookies` | lembrar o último e-mail no login |
| Flash com categoria | `flash(..., "erro")` / `flash(..., "sucesso")` + `base.html` |
| Validação no back-end (vazio, tamanho, número) | `ler_formulario()` e rotas de cadastro/avaliação |
| `@app.errorhandler(404)` | `app/__init__.py` + `app/views/404.html` |
| `app.logger` | login, falha de login, cadastro, criação e exclusão |
| **Extras:** edição, busca, relacionamento, visual | editar filme, busca por título, avaliação ligada ao filme, tema Y2K, testes |

---

## 🧩 Explicando cada parte

### 1. `app/db.py` — a classe `DatabaseConnection`
É **exatamente o padrão da Aula 15**. Ela é usada com `with`:
```python
with DatabaseConnection() as db:
    db.cursor.execute("SELECT ...", (valor,))
```
- `__enter__` roda quando o `with` começa: abre o banco, liga o `row_factory` (para usar `linha["titulo"]`),
  cria o cursor e ativa as **chaves estrangeiras** (`PRAGMA foreign_keys = ON`).
- `__exit__` roda quando o `with` termina: se deu tudo certo faz `commit()`, se deu erro faz `rollback()`
  (desfaz), e **sempre** fecha a conexão.

👉 Por isso os Models **não precisam** chamar `commit()` nem `close()`: o `with` faz sozinho.

### 2. `iniciar_bd.py` — cria o banco
- `TABELAS`: o SQL das 3 tabelas (`usuarios`, `filmes`, `avaliacoes`) com `CREATE TABLE IF NOT EXISTS`,
  `INTEGER PRIMARY KEY AUTOINCREMENT` e `FOREIGN KEY ... ON DELETE CASCADE`.
- `criar_tabelas()`: executa esse SQL.
- `criar_dados_iniciais()`: cria a usuária de teste com `Usuario(...).salvar()` e grava os 10 filmes dela.
  Se ela já existir, não faz nada, então dá para rodar o script de novo **sem duplicar**.

**ON DELETE CASCADE** quer dizer: se apagar um filme, as avaliações dele são apagadas junto.

### 3. Models (`app/models/`)
Cada classe tem os dados (`__init__`) e os métodos com o SQL.

| Classe | Métodos |
|---|---|
| `Usuario` | `salvar()`, `buscar_por_id()`, `buscar_por_email()` |
| `Filme` | `salvar()` (INSERT), `atualizar()` (UPDATE), `excluir()`, `listar_por_usuario()`, `buscar_por_id()` |
| `Avaliacao` | `salvar()`, `excluir()`, `listar_por_usuario()`, `listar_por_filme()`, `buscar_por_id()` |

- Todo SQL usa `?` com tupla, o que **evita SQL Injection**.
- A busca por título usa `LIKE '%' || ? || '%'`. O `||` junta textos **dentro do SQL**, então o valor continua
  indo pelo `?` (o PDF proíbe f-string no SQL).
- `Avaliacao.listar_por_usuario()` usa um **JOIN** com `filmes` para mostrar o título do filme.

### 4. Controllers (`app/controllers/`)
Três blueprints: `auth_bp`, `filmes_bp` e o novo `avaliacoes_bp`. **Nenhuma linha de SQL.**
Cada rota: lê o `request` → valida → chama o Model → `render_template` ou `redirect(url_for(...))`.

Rotas novas de avaliações:
| Rota | O que faz |
|---|---|
| `GET /avaliacoes` | lista as minhas avaliações |
| `POST /filmes/<id>/avaliacoes` | cria uma avaliação (formulário na página do filme) |
| `POST /avaliacoes/<id>/excluir` | exclui uma avaliação |

### 5. Middleware — `app/utils/auth_middleware.py`
O `@login_required`:
1. pega o `session.get("user_id")`;
2. **confere no banco** com `Usuario.buscar_por_id()`;
3. se existir, guarda a usuária em **`g.usuario`** e deixa a rota rodar;
4. se não, limpa a sessão, mostra um flash e manda para o login.

As rotas usam `g.usuario.id` para saber de quem são os filmes.

### 6. Sessão
- Login: `session.clear()`, depois `session["user_id"]` e `session["username"]`.
- Logout: `session.clear()`.
- `app.secret_key` fica no `app/__init__.py`.

### 7. Cookie (Aula 14)
Ao logar, o site grava o cookie `ultimo_email` por **30 dias** (`set_cookie` com `max_age`).
Na próxima vez que abrir o login, o campo de e-mail **já vem preenchido** (`request.cookies.get("ultimo_email")`).

### 8. Validações no back-end
| Campo | Regra |
|---|---|
| Nome (cadastro) | obrigatório, até 60 caracteres |
| Senha | mínimo 6, confirmação igual |
| Filme | título até 100, mood até 40, sinopse até 1000, ano entre 1900 e 2100 |
| Avaliação | nota de 1 a 5, comentário até 500 |

### 9. Erro 404 e logs
- `@app.errorhandler(404)` mostra a página `404.html`, no tema do site. Ela aparece também quando alguém tenta
  abrir um filme que **não é seu**.
- `current_app.logger` registra no terminal: login, falha de login, cadastro de usuária, filme cadastrado/excluído,
  avaliação criada/excluída. Exemplo:
  ```
  INFO in auth_controller: Login realizado: diva@cinedivas.com
  ```

### 10. Testes (`tests/test_app.py`)
21 testes automáticos. Para rodar: `python -m unittest -v`.
Eles conferem: o `iniciar_bd.py`, o hash da senha, sessão, cookie, middleware, CRUD de filmes, avaliações,
cascata, validações, que uma usuária **não vê nem apaga** o que é de outra, e o 404.

---

## 🎤 Justificativas para falar no vídeo (o PDF pede)

| Mudança em relação ao padrão das aulas | Por quê |
|---|---|
| `session["username"]` guarda o **nome** da usuária | O login é por e-mail, então não existe campo `username`. O nome cumpre o mesmo papel (mostrar "oi, fulana"). |
| `DB_PATH` lê a variável de ambiente `DB_PATH` | Para os testes usarem um banco temporário e não mexerem no banco real. Sem a variável, o caminho é o mesmo do padrão. |
| `Flask(__name__, template_folder="views")` | O PDF pede a pasta `views/`, mas o Flask procura `templates/` por padrão. |
| Busca com `LIKE '%' \|\| ? \|\| '%'` | Para não usar f-string no SQL e continuar com o valor no `?`. |
| Usuária nova começa sem filmes | Cada usuária só vê o que é dela (`usuario_id`). Os 10 filmes iniciais são da usuária de teste. |
| `Filme` tem `salvar()` e `atualizar()` separados | Segue os nomes de métodos do PDF e fica mais fácil de explicar. |

---

## 🧹 O que saiu do projeto (versão anterior)
- `get_db()`, `close_db()` e `init_app()` do `db.py` → trocados pela `DatabaseConnection`.
- Criação das tabelas ao abrir o site → agora é só no `iniciar_bd.py`.
- `use_reloader=False` no `run.py` → não precisa mais (o site não cria tabelas). Voltou o `app.run(debug=True)`.
- `login_obrigatorio` dentro do `auth_controller.py` → virou `login_required` em `app/utils/`.
- `views/` e `static/` na raiz → foram para dentro de `app/`, como no PDF.
- `ESTUDO_filme_db.md` → removido, porque explicava o código antigo. Este documento substitui.

---

## 📦 O que falta VOCÊ fazer para entregar (até 24/11 às 00h00, no Moodle)

- [ ] Preencher o arquivo **`RESUMO_ENTREGA.txt`** com seu **nome completo**, **prontuário** e os dois links.
- [ ] Deixar o repositório do GitHub **público**.
- [ ] Gravar o **vídeo de até 5 minutos** (siga o `ROTEIRO_VIDEO.md`) e colocar no YouTube (não listado) ou
      no Google Drive com acesso "Qualquer pessoa com o link".
- [ ] Enviar o resumo (PDF, DOCX ou TXT) no Moodle.
