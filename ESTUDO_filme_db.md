# 📚 Guia de estudo — `filme.py` e `db.py` linha a linha

> Material para a Alice estudar e explicar ao professor.
> Os números de linha batem com os arquivos [app/models/filme.py](app/models/filme.py) e [app/db.py](app/db.py).

---

## Visão geral (comece por aqui)

| Arquivo | Para que serve | Qual tabela |
|---|---|---|
| `app/models/filme.py` | Classe **`Filme`**: o modelo (POO) que guarda os dados de um filme **e** todo o SQL da tabela `filmes` (criar, inserir, atualizar, apagar, listar, buscar). | `filmes` |
| `app/db.py` | Funções de apoio para a conexão com o banco usada no **login/cadastro de usuárias**. Também cria a tabela `usuarios`. | `usuarios` |

Os dois usam a biblioteca **`sqlite3`**, que já vem com o Python. **Não tem ORM** (nada de SQLAlchemy): todo SQL é escrito na mão.
O banco é um único arquivo: `instance/cine_divas.db`.

---

# Parte 1 — `app/models/filme.py`

## Linhas 1–3: importações

```python
1  import sqlite3
2
3  from flask import current_app
```

| Linha | O que faz |
|---|---|
| 1 | Importa o **`sqlite3`**, biblioteca nativa do Python para falar com bancos SQLite. É com ela que a gente abre a conexão e roda SQL. |
| 2 | Linha em branco (só organização). |
| 3 | Importa o **`current_app`** do Flask: é "o app Flask que está rodando agora". A gente usa para ler a configuração `DATABASE` (o caminho do arquivo `.db`), definida em `app/__init__.py`. |

---

## Linhas 6–7: a classe

```python
6  class Filme:
7      """Representa um filme e concentra TODO o acesso à tabela `filmes` (sqlite3 puro, sem ORM)."""
```

| Linha | O que faz |
|---|---|
| 6 | Cria a **classe `Filme`**. Uma classe é um "molde": cada filme do site vira um **objeto** criado a partir desse molde. |
| 7 | **Docstring** (texto entre três aspas): é só documentação, explica para que a classe serve. Não executa nada. |

---

## Linhas 9–16: o construtor `__init__`

```python
9   def __init__(self, titulo, ano, mood, sinopse, emoji="🎬", poster="", id=None):
10      self.id = id
11      self.titulo = titulo
12      self.ano = ano
13      self.mood = mood
14      self.sinopse = sinopse
15      self.emoji = emoji
16      self.poster = poster
```

| Linha | O que faz |
|---|---|
| 9 | **`__init__`** é o **construtor**: roda automaticamente quando a gente escreve `Filme(...)`. Recebe os dados do filme. **`self`** é o próprio objeto que está sendo criado. `emoji`, `poster` e `id` têm **valor padrão** (`"🎬"`, `""`, `None`), então são opcionais. |
| 10 | Guarda o `id` dentro do objeto. Um filme **novo** chega com `id=None` (ainda não está no banco). Um filme que **veio do banco** chega com o `id` dele (1, 2, 3...). |
| 11–16 | Guardam cada dado como um **atributo** do objeto (`self.titulo`, `self.ano`...). Depois dá para usar `filme.titulo` em qualquer lugar, inclusive no HTML (`{{ filme.titulo }}`). |

> 💡 **Exemplo:** `f = Filme("Titanic", 1997, "Para chorar", "Jack e Rose...")` cria um objeto com `f.id == None` e `f.titulo == "Titanic"`.

---

## Linhas 18–25: `conectar()`

```python
18  # ---------- conexão e tabela ----------
19
20  @staticmethod
21  def conectar():
22      """Abre uma conexão com o arquivo .db configurado no app."""
23      conexao = sqlite3.connect(current_app.config["DATABASE"])
24      conexao.row_factory = sqlite3.Row  # permite acessar colunas pelo nome: linha["titulo"]
25      return conexao
```

| Linha | O que faz |
|---|---|
| 18 | Comentário (`#`): só separa as seções do arquivo. |
| 20 | **`@staticmethod`**: este método **não precisa** de um objeto (`self`) nem da classe (`cls`). É uma função que "mora" dentro da classe. Pode ser chamado como `Filme.conectar()` ou `self.conectar()`. |
| 21 | Define o método `conectar`. |
| 22 | Docstring explicando o método. |
| 23 | **`sqlite3.connect(...)`** abre a conexão com o arquivo `.db`. O caminho vem de `current_app.config["DATABASE"]` (= `instance/cine_divas.db`). Se o arquivo não existir, o SQLite **cria** ele. |
| 24 | **`row_factory = sqlite3.Row`**: faz cada linha do resultado se comportar como um dicionário. Sem isso, a linha seria uma tupla `(1, "Titanic", ...)` e a gente teria que usar `linha[1]`. Com isso, dá para usar `linha["titulo"]`, e dá para converter com `dict(linha)`. |
| 25 | Devolve a conexão para quem chamou (os outros métodos usam ela para rodar SQL). |

---

## Linhas 27–47: `criar_tabela()`

```python
27  @classmethod
28  def criar_tabela(cls):
29      """Cria a tabela (se não existir) e, se estiver vazia, grava os 10 filmes iniciais."""
30      conexao = cls.conectar()
31      conexao.execute("""
32          CREATE TABLE IF NOT EXISTS filmes (
33              id      INTEGER PRIMARY KEY AUTOINCREMENT,
34              titulo  TEXT NOT NULL,
35              ano     INTEGER NOT NULL,
36              mood    TEXT NOT NULL,
37              sinopse TEXT NOT NULL,
38              emoji   TEXT NOT NULL DEFAULT '🎬',
39              poster  TEXT NOT NULL DEFAULT ''
40          )
41      """)
42      total = conexao.execute("SELECT COUNT(*) FROM filmes").fetchone()[0]
43      conexao.close()
44
45      if total == 0:
46          for dados in FILMES_INICIAIS:
47              cls(**dados).salvar()
```

| Linha | O que faz |
|---|---|
| 27 | **`@classmethod`**: o método recebe a **classe** (`cls`) em vez de um objeto. Usado porque criar a tabela não é coisa de *um* filme, é da classe toda. Chamado como `Filme.criar_tabela()` (isso acontece em `app/__init__.py`, quando o site liga). |
| 28 | Define o método. `cls` aqui é a própria classe `Filme`. |
| 29 | Docstring. |
| 30 | Abre a conexão usando o método `conectar()`. |
| 31 | **`conexao.execute(...)`** roda um comando SQL. O SQL está entre `"""` (texto de várias linhas). |
| 32 | **`CREATE TABLE IF NOT EXISTS filmes`**: cria a tabela `filmes` **só se ela ainda não existir**. Assim dá para rodar toda vez que o site liga, sem dar erro. |
| 33 | Coluna `id`: número inteiro, **chave primária** (identifica cada filme, não repete) e **AUTOINCREMENT** (o banco gera 1, 2, 3... sozinho, e nunca reaproveita um número apagado). |
| 34 | Coluna `titulo`: texto, **NOT NULL** (obrigatório, não pode ficar vazio/nulo). |
| 35 | Coluna `ano`: número inteiro, obrigatório. |
| 36 | Coluna `mood`: texto, obrigatório ("Para rir", "Para chorar"...). |
| 37 | Coluna `sinopse`: texto, obrigatório. |
| 38 | Coluna `emoji`: texto, obrigatório, mas com **DEFAULT '🎬'** (se não mandar nada, o banco põe 🎬). |
| 39 | Coluna `poster`: texto, obrigatório, com valor padrão `''` (vazio). Guarda `img/arquivo.jpg` ou um link `http...`. |
| 40–41 | Fecham o `CREATE TABLE` e o `execute`. |
| 42 | **`SELECT COUNT(*) FROM filmes`** conta quantos filmes tem na tabela. **`fetchone()`** pega a primeira (e única) linha do resultado, e **`[0]`** pega o primeiro valor dela (o número). Guarda em `total`. |
| 43 | **Fecha a conexão** (sempre fechar depois de usar). |
| 45 | Se a tabela está **vazia** (primeira vez que o site roda)... |
| 46 | ...percorre cada dicionário da lista `FILMES_INICIAIS` (os 10 filmes do fim do arquivo)... |
| 47 | ...e para cada um: **`cls(**dados)`** cria um objeto `Filme`. O **`**`** "desempacota" o dicionário: `{"titulo": "X", "ano": 2003}` vira `Filme(titulo="X", ano=2003)`. Depois chama **`.salvar()`**, que faz o `INSERT`. |

> 💡 Por isso os 10 filmes só são gravados **uma vez**. Da segunda vez em diante, `total` já é 10 e o `if` não entra.

---

## Linhas 49–66: `salvar()` (Create e Update)

```python
49  # ---------- escrita (Create / Update / Delete) ----------
50
51  def salvar(self):
52      """INSERT se o filme ainda não tem id; UPDATE se já existe no banco."""
53      conexao = self.conectar()
54      if self.id is None:
55          cursor = conexao.execute(
56              "INSERT INTO filmes (titulo, ano, mood, sinopse, emoji, poster) VALUES (?, ?, ?, ?, ?, ?)",
57              (self.titulo, self.ano, self.mood, self.sinopse, self.emoji, self.poster),
58          )
59          self.id = cursor.lastrowid
60      else:
61          conexao.execute(
62              "UPDATE filmes SET titulo = ?, ano = ?, mood = ?, sinopse = ?, emoji = ?, poster = ? WHERE id = ?",
63              (self.titulo, self.ano, self.mood, self.sinopse, self.emoji, self.poster, self.id),
64          )
65      conexao.commit()
66      conexao.close()
```

| Linha | O que faz |
|---|---|
| 51 | Método **normal** (de objeto): recebe `self`, ou seja, o filme que vai ser salvo. Chamado como `filme.salvar()`. |
| 52 | Docstring. |
| 53 | Abre a conexão. |
| 54 | **Decide se é novo ou existente:** se o objeto **não tem `id`**, ele ainda não está no banco, então é um **cadastro** (INSERT). |
| 55 | Roda o SQL e guarda o **`cursor`** (o objeto que o `execute` devolve; usado na linha 59). |
| 56 | **`INSERT INTO filmes (...) VALUES (?, ?, ...)`**: insere uma linha nova. Cada **`?`** é um **espaço reservado** que o sqlite3 preenche com os valores da linha 57, na mesma ordem. Não passamos o `id`, porque o banco gera sozinho (AUTOINCREMENT). |
| 57 | **Tupla** com os valores que vão nos `?`: o 1º `?` recebe `self.titulo`, o 2º recebe `self.ano`, e assim por diante. |
| 59 | **`cursor.lastrowid`** é o `id` que o banco acabou de gerar. A gente guarda no objeto, que agora "sabe" qual é o seu id. |
| 60 | **Senão** (o objeto já tem `id`), é uma **edição**... |
| 61–63 | **`UPDATE filmes SET ... WHERE id = ?`**: altera as colunas **só da linha com aquele id**. O último `?` recebe `self.id`. ⚠️ Sem o `WHERE`, alteraria **todos** os filmes! |
| 65 | **`conexao.commit()`** **confirma** a gravação no arquivo `.db`. Sem o `commit`, a alteração fica pendente e é **perdida** ao fechar. |
| 66 | Fecha a conexão. |

---

## Linhas 68–72: `excluir()` (Delete)

```python
68  def excluir(self):
69      conexao = self.conectar()
70      conexao.execute("DELETE FROM filmes WHERE id = ?", (self.id,))
71      conexao.commit()
72      conexao.close()
```

| Linha | O que faz |
|---|---|
| 68 | Método de objeto: apaga **este** filme. Chamado como `filme.excluir()`. |
| 69 | Abre a conexão. |
| 70 | **`DELETE FROM filmes WHERE id = ?`** apaga a linha com o id do filme. Note o **`(self.id,)`** com **vírgula**: é uma tupla de **um** elemento. Sem a vírgula, `(self.id)` seria só um número entre parênteses, e o sqlite3 exige uma tupla. |
| 71 | `commit()` para confirmar a exclusão no arquivo. |
| 72 | Fecha a conexão. |

---

## Linhas 74–85: `listar()` (Read: vários filmes)

```python
74  # ---------- leitura (Read) ----------
75
76  @classmethod
77  def listar(cls, busca=""):
78      """Retorna uma lista de objetos Filme vindos do banco (com filtro opcional por título)."""
79      conexao = cls.conectar()
80      linhas = conexao.execute(
81          "SELECT * FROM filmes WHERE titulo LIKE ? ORDER BY id",
82          (f"%{busca}%",),
83      ).fetchall()
84      conexao.close()
85      return [cls(**dict(linha)) for linha in linhas]
```

| Linha | O que faz |
|---|---|
| 76 | `@classmethod`: listar não depende de um filme específico, é da classe. Chamado como `Filme.listar()`. |
| 77 | Recebe `busca` (o texto digitado na caixa de busca). Padrão `""` = sem filtro. |
| 79 | Abre a conexão. |
| 81 | **`SELECT * FROM filmes`** busca todas as colunas (`*`) da tabela. **`WHERE titulo LIKE ?`** filtra pelo título. **`ORDER BY id`** ordena pelo id (ordem de cadastro). |
| 82 | O valor do `?`: **`f"%{busca}%"`** é uma **f-string** que coloca `%` antes e depois do texto. No `LIKE`, `%` significa "qualquer coisa". Então `%loira%` acha "Legalmente **Loira**". Se `busca` for vazio, fica `%%`, que acha **todos**. |
| 83 | **`.fetchall()`** pega **todas** as linhas do resultado (uma lista). |
| 84 | Fecha a conexão. |
| 85 | **List comprehension**: para cada `linha` do resultado, faz `dict(linha)` (vira dicionário, graças ao `row_factory` da linha 24) e `cls(**...)` (vira um objeto `Filme`). Devolve uma **lista de objetos `Filme`**. É essa lista que o template percorre com `{% for filme in filmes %}`. |

> 💡 A linha 85 é o mesmo que:
> ```python
> resultado = []
> for linha in linhas:
>     resultado.append(Filme(**dict(linha)))
> return resultado
> ```

---

## Linhas 87–92: `buscar_por_id()` (Read: um filme)

```python
87  @classmethod
88  def buscar_por_id(cls, id):
89      conexao = cls.conectar()
90      linha = conexao.execute("SELECT * FROM filmes WHERE id = ?", (id,)).fetchone()
91      conexao.close()
92      return cls(**dict(linha)) if linha else None
```

| Linha | O que faz |
|---|---|
| 87–88 | `@classmethod` que recebe o `id` do filme procurado. Chamado como `Filme.buscar_por_id(3)`. Usado na página de detalhe, na edição e na exclusão. |
| 89 | Abre a conexão. |
| 90 | **`SELECT * FROM filmes WHERE id = ?`** busca o filme com aquele id. **`.fetchone()`** pega **uma** linha só (ou `None` se não achou). |
| 91 | Fecha a conexão. |
| 92 | **If de uma linha (ternário):** se achou (`linha` existe), transforma em objeto `Filme` e devolve. Se não achou, devolve **`None`**. A rota usa esse `None` para mostrar o erro **404**. |

---

## Linhas 95 em diante: `FILMES_INICIAIS`

```python
95  # seed de filmes para popular o banco
96  FILMES_INICIAIS = [
97      {
98          "titulo": "Como Perder um Homem em 10 Dias",
...
```

| Linha | O que faz |
|---|---|
| 95 | Comentário: "seed" significa **semente**, os dados iniciais para popular o banco. |
| 96+ | Lista com 10 **dicionários**, um por filme. Cada chave (`"titulo"`, `"ano"`...) tem **o mesmo nome** de um parâmetro do `__init__`, por isso funciona o `Filme(**dados)` da linha 47. |

> ⚠️ **Importante para o professor:** essa lista **não é usada para mostrar filmes na tela**. Ela é lida **uma única vez**, pela `criar_tabela()`, quando a tabela está vazia. Depois disso, tudo que aparece na listagem vem do `SELECT` em `listar()`.

> ❓ "Mas a lista está no fim do arquivo e é usada na linha 46, lá em cima. Como funciona?"
> O Python lê o arquivo todo **antes** de alguém chamar `criar_tabela()`. Quando o método roda de verdade (no `create_app`), a lista já existe.

---

# Parte 2 — `app/db.py`

Este arquivo cuida da conexão usada pelo **login e cadastro de usuárias** (`auth_controller.py`) e cria a tabela `usuarios`.

## Linhas 1–3: importações

```python
1  import sqlite3
2
3  from flask import current_app, g
```

| Linha | O que faz |
|---|---|
| 1 | Importa o `sqlite3` (mesma biblioteca do `filme.py`). |
| 3 | Importa `current_app` (o app rodando, para ler o caminho do banco) e **`g`**: um "objeto de rascunho" do Flask que **vive só durante uma requisição** (um clique, um envio de formulário). Serve para guardar a conexão e reaproveitar durante aquela requisição. |

---

## Linhas 5–13: `SCHEMA` (a estrutura da tabela de usuárias)

```python
5   SCHEMA = """
6   CREATE TABLE IF NOT EXISTS usuarios (
7       id         INTEGER PRIMARY KEY AUTOINCREMENT,
8       nome       TEXT NOT NULL,
9       email      TEXT UNIQUE NOT NULL,
10      senha_hash TEXT NOT NULL,
11      criado_em  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
12  );
13  """
```

| Linha | O que faz |
|---|---|
| 5 | Cria a variável **`SCHEMA`** com um texto de várias linhas contendo o SQL. "Schema" = estrutura do banco. Por ser só um texto, ainda **não executa nada** (quem executa é a linha 32). |
| 6 | Cria a tabela `usuarios` se ainda não existir. |
| 7 | `id`: chave primária com numeração automática. |
| 8 | `nome`: texto obrigatório. |
| 9 | `email`: texto obrigatório e **UNIQUE** (o banco **não deixa** dois cadastros com o mesmo e-mail). Se tentar, dá erro `IntegrityError`, que o `auth_controller.py` captura para mostrar "Já existe uma conta com esse e-mail". |
| 10 | `senha_hash`: guarda a senha **hasheada** (embaralhada de forma irreversível, com `generate_password_hash`). **Nunca** a senha de verdade. |
| 11 | `criado_em`: data/hora do cadastro. **`DEFAULT CURRENT_TIMESTAMP`** = o banco preenche sozinho com o momento atual. |
| 12–13 | Fecham o comando (`;`) e o texto. |

---

## Linhas 16–20: `get_db()`

```python
16  def get_db():
17      if "db" not in g:
18          g.db = sqlite3.connect(current_app.config["DATABASE"])
19          g.db.row_factory = sqlite3.Row
20      return g.db
```

| Linha | O que faz |
|---|---|
| 16 | Função que **entrega uma conexão** com o banco. |
| 17 | Se **ainda não existe** uma conexão guardada no `g` nesta requisição... |
| 18 | ...abre uma nova com `sqlite3.connect` e guarda em `g.db`. |
| 19 | Mesmo truque do `filme.py`: acessar colunas pelo nome (`usuario["email"]`). |
| 20 | Devolve a conexão. Se a função for chamada **de novo na mesma requisição**, ela pula o `if` e **reaproveita** a mesma conexão (não abre outra). |

---

## Linhas 23–26: `close_db()`

```python
23  def close_db(error=None):
24      conexao = g.pop("db", None)
25      if conexao is not None:
26          conexao.close()
```

| Linha | O que faz |
|---|---|
| 23 | Função que **fecha** a conexão. Recebe `error` porque o Flask passa o erro (se houve algum) quando chama ela no fim da requisição. A gente não usa, mas o parâmetro precisa existir. |
| 24 | **`g.pop("db", None)`** **tira** a conexão de dentro do `g` e devolve ela. Se não existir, devolve `None` (em vez de dar erro). |
| 25 | Se havia uma conexão aberta... |
| 26 | ...fecha. |

---

## Linhas 29–35: `init_app()`

```python
29  def init_app(app):
30      with app.app_context():
31          conexao = get_db()
32          conexao.executescript(SCHEMA)
33          conexao.commit()
34          close_db()
35      app.teardown_appcontext(close_db)
```

| Linha | O que faz |
|---|---|
| 29 | Função chamada **uma vez** quando o site liga (em `app/__init__.py`: `db.init_app(app)`). Recebe o app Flask. |
| 30 | **`with app.app_context():`** "liga" o contexto do app. Fora de uma requisição, o `current_app` e o `g` não existem. Esse `with` faz eles existirem por um momento, para a gente poder usar o `get_db()`. |
| 31 | Pega uma conexão. |
| 32 | **`executescript(SCHEMA)`** roda o SQL do `SCHEMA` (cria a tabela `usuarios`, se não existir). Diferença: `execute` roda **um** comando; `executescript` roda um **texto com vários** comandos separados por `;`. |
| 33 | `commit()` para confirmar. |
| 34 | Fecha a conexão. |
| 35 | **`teardown_appcontext(close_db)`** registra o `close_db` para o Flask chamar **automaticamente no fim de toda requisição**. Assim a conexão do login/cadastro sempre é fechada, mesmo se der erro. |

---

# Parte 3 — Perguntas que o professor pode fazer

**Por que não usou SQLAlchemy?**
A regra da atividade proíbe ORM. Usei só `sqlite3`, que já vem no Python, com SQL escrito na mão (`CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`).

**Onde está o SQL dos filmes?**
Todo dentro da classe `Filme` (`app/models/filme.py`). As rotas em `filmes_controller.py` não têm SQL: só criam o objeto e chamam `salvar()`, `excluir()`, `listar()` ou `buscar_por_id()`.

**Para que serve o `?` no SQL?**
É um espaço reservado. O `sqlite3` coloca os valores no lugar de forma segura, o que **evita SQL Injection** (alguém digitar um comando SQL no formulário e ele ser executado).

**Para que serve o `commit()`?**
Confirma a gravação no arquivo. `INSERT`, `UPDATE` e `DELETE` precisam de `commit`. `SELECT` não precisa, porque só lê.

**Por que fechar a conexão (`close()`)?**
Para liberar o arquivo do banco e não deixar conexões abertas acumulando.

**Como o `salvar()` sabe se é cadastro ou edição?**
Pelo `id`. Filme novo tem `id = None`, então faz `INSERT`. Filme que veio do banco já tem `id`, então faz `UPDATE ... WHERE id = ?`.

**Qual a diferença entre `self` e `cls`?**
`self` é **um objeto** (um filme específico), usado em `salvar()` e `excluir()`. `cls` é a **classe** `Filme`, usada em `criar_tabela()`, `listar()` e `buscar_por_id()`, que não dependem de um filme específico (e, no caso das buscas, criam objetos novos com `cls(...)`).

**E o `@staticmethod` do `conectar()`?**
Ele não precisa nem de `self` nem de `cls`: só abre a conexão. Fica dentro da classe para manter todo o acesso ao banco junto.

**O que é `row_factory = sqlite3.Row`?**
Faz as linhas do resultado se comportarem como dicionários, permitindo `linha["titulo"]` e `dict(linha)`. Sem isso viriam tuplas, e eu teria que lembrar a posição de cada coluna.

**O que o `**dados` faz?**
Desempacota um dicionário em parâmetros nomeados: `Filme(**{"titulo": "X", "ano": 2003, ...})` é igual a `Filme(titulo="X", ano=2003, ...)`.

**Por que existe a lista `FILMES_INICIAIS` se é proibido lista em memória?**
Ela só **popula** o banco na primeira vez, quando a tabela está vazia (é uma "seed"). A listagem da tela vem sempre do `SELECT` em `Filme.listar()`. Se eu cadastrar um filme novo, ele aparece porque foi gravado no banco, não porque está na lista.

**Por que tem dois jeitos de conectar (`db.py` e `Filme.conectar()`)?**
O `db.py` é o jeito que o Flask recomenda e é usado pelo login/cadastro de usuárias: guarda a conexão no `g` e fecha sozinho no fim da requisição. A classe `Filme` tem o próprio `conectar()` porque a atividade pede que **a classe contenha todo o acesso ao banco**, então cada método abre, usa e fecha a sua conexão.

**O que acontece quando eu clico em "salvar" no cadastro de filme?**
1. O formulário (`filme_form.html`) envia um `POST` para `/filmes/novo`.
2. A rota `novo()` lê os campos com `ler_formulario()` e valida.
3. Cria o objeto: `filme = Filme(**dados)`, que ainda está sem `id`.
4. Chama `filme.salvar()`: `conectar()`, `INSERT INTO filmes ...`, `commit()`, `close()`.
5. Redireciona para `/filmes`, onde `Filme.listar()` faz o `SELECT` e o template mostra o filme novo com `{% for %}`.
