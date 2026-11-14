# 📚 Guia de estudo — banco de dados do Cine Divas

> Material para a Alice explicar ao professor. Os números de linha batem com
> [app/db.py](app/db.py), [app/models/filme.py](app/models/filme.py) e [app/models/usuario.py](app/models/usuario.py).

## A ideia em 3 frases

1. **Um banco só**: o arquivo `instance/cine_divas.db` tem as duas tabelas (`usuarios` e `filmes`).
2. **`db.py` cuida da conexão e cria as tabelas uma única vez**, quando o site abre.
3. **Cada tabela tem uma classe com o seu SQL**: `Filme` e `Usuario`. As rotas não escrevem SQL, só chamam a classe.

```
rota (controller)  →  classe (Filme / Usuario)  →  get_db() do db.py  →  arquivo .db
```

---

## `app/db.py`

| Linhas | O que faz |
|---|---|
| 1 | `import sqlite3`: biblioteca do Python para SQLite. Sem ORM. |
| 3 | `current_app` = o app rodando (de onde vem o caminho do banco). `g` = "rascunho" do Flask que dura **uma requisição**. |
| 10–27 | **`SCHEMA`**: o SQL que cria as **duas tabelas**. `CREATE TABLE IF NOT EXISTS` só cria se ainda não existir. É só texto; quem executa é a linha 118. |
| 12, 19 | `id INTEGER PRIMARY KEY AUTOINCREMENT`: o banco gera o id sozinho (1, 2, 3...). |
| 14 | `email ... UNIQUE`: o banco recusa e-mail repetido (dá `sqlite3.IntegrityError`). |
| 15 | `senha_hash`: guarda a senha embaralhada (hash), nunca a senha real. |
| 24–25 | `DEFAULT`: valor usado quando nada é enviado. |
| 35–86 | **`FILMES_INICIAIS`**: os 10 filmes, cada um uma tupla na ordem das colunas. Só usados para encher a tabela vazia. |
| 93–98 | **`get_db()`**: entrega a conexão. Na 1ª vez da requisição, abre (`sqlite3.connect`) e guarda em `g.db`. Nas próximas, reaproveita a mesma. |
| 97 | `row_factory = sqlite3.Row`: permite `linha["titulo"]` e `dict(linha)`. |
| 101–105 | **`close_db()`**: tira a conexão do `g` e fecha. O Flask chama sozinho no fim de cada requisição. |
| 112 | **`init_app(app)`**: chamada **uma vez**, em `create_app()` (`app/__init__.py`). |
| 114 | Registra o `close_db` para rodar no fim de toda requisição. |
| 116 | `with app.app_context()`: "liga" o app, para o `get_db()` funcionar fora de uma requisição. |
| 118 | `executescript(SCHEMA)`: executa o SQL das duas tabelas. (`executescript` roda vários comandos de uma vez.) |
| 120 | Conta quantos filmes existem. `fetchone()[0]` = o número. |
| 121–125 | Se a tabela está vazia, `executemany` faz um `INSERT` para **cada** tupla de `FILMES_INICIAIS`. |
| 127 | `commit()`: confirma tudo no arquivo. |

### Por que as tabelas são criadas uma única vez?
- `init_app()` só é chamada em um lugar: `create_app()`.
- No `run.py` está `app.run(debug=True, use_reloader=False)`. Com o reloader ligado (padrão do `debug=True`),
  o Flask abre o programa **2 vezes** (dois processos), e as tabelas seriam criadas duas vezes. Desligado, roda uma vez.
- E mesmo que rodasse de novo: `IF NOT EXISTS` não recria, e os filmes só entram se `total == 0`. Nada duplica.

---

## `app/models/filme.py`

| Linhas | O que faz |
|---|---|
| 1 | Importa `get_db`: a classe usa **a mesma conexão** do resto do projeto. |
| 4–5 | Classe **`Filme`**: um filme + todo o SQL da tabela `filmes`. |
| 7–14 | **`__init__`**: construtor. Guarda os dados no objeto (`self`). Filme novo vem com `id=None`. |
| 16 | **`salvar()`**: Create e Update. |
| 19 | `valores`: tupla com os dados, na ordem das colunas (usada nos dois SQLs, sem repetir). |
| 21–26 | Sem `id` = filme novo: `INSERT`. Os `?` recebem os `valores` (protege contra SQL Injection). `cursor.lastrowid` = id que o banco gerou. |
| 27–31 | Com `id` = edição: `UPDATE ... WHERE id = ?`. `valores + (self.id,)` junta o id no fim, para o último `?`. |
| 33 | `commit()`: sem ele nada é gravado. |
| 35–38 | **`excluir()`**: `DELETE ... WHERE id = ?` + `commit()`. `(self.id,)` tem vírgula porque precisa ser tupla. |
| 40–46 | **`listar(busca)`**: `SELECT` com `LIKE`. `%` = "qualquer coisa", então `%loira%` acha "Legalmente Loira". `fetchall()` pega todas as linhas, e a última linha transforma cada uma em objeto `Filme`. |
| 48–52 | **`buscar_por_id(id)`**: `SELECT ... WHERE id = ?`. `fetchone()` pega uma linha. Devolve o `Filme` ou `None` (a rota mostra 404). |

`@classmethod` (linhas 40 e 48): o método é chamado pela **classe** (`Filme.listar()`), porque ainda não existe um filme;
ele recebe `cls` e usa `cls(...)` para criar os objetos.

---

## `app/models/usuario.py`

Mesmo padrão do `Filme`, para a tabela `usuarios`.

| Linhas | O que faz |
|---|---|
| 7–12 | **`__init__`**: guarda nome, e-mail, hash da senha, id e data de criação. |
| 14–22 | **`salvar()`**: `INSERT INTO usuarios` + `commit()`. Se o e-mail já existir, o banco lança `IntegrityError`, que a rota de cadastro trata. |
| 24–28 | **`buscar_por_email()`**: usado no login. Devolve a `Usuario` ou `None`. |

---

## O caminho do dado (clique em "salvar" no cadastro de filme)

1. `filme_form.html` envia um `POST` para `/filmes/novo`.
2. A rota `novo()` lê e valida o formulário (`ler_formulario()`).
3. `filme = Filme(**dados)` cria o objeto (sem id).
4. `filme.salvar()` chama `get_db()` → `INSERT` → `commit()`.
5. Redireciona para `/filmes`. `Filme.listar()` faz o `SELECT` e o template mostra com `{% for filme in filmes %}`.
6. No fim da requisição, o Flask chama `close_db()` e a conexão é fechada.

---

## Perguntas prováveis

**O que mudou para "unificar o banco"?** Antes havia dois jeitos de conectar (um no `db.py` e outro dentro da classe `Filme`)
e funções de SQL repetidas no `db.py`. Agora existe **uma conexão** (`get_db`) e **um lugar que cria as tabelas** (`init_app`).

**Onde fica o SQL?** Dentro das classes `Filme` e `Usuario`. As rotas só chamam os métodos.

**Por que `?` no SQL?** O `sqlite3` coloca os valores de forma segura, evitando SQL Injection.

**Por que `commit()`?** Confirma a gravação no arquivo. `SELECT` não precisa.

**Quem fecha a conexão?** O `close_db()`, que o Flask chama sozinho no fim de cada requisição (linha 114 do `db.py`).

**Como você testou?** Com `python -m unittest -v`. Os testes (`tests/test_app.py`) usam um banco temporário e verificam
cadastro, login, listagem, cadastrar/editar/excluir filme, busca e que os filmes iniciais não duplicam.
