# 🎬 Roteiro do vídeo — Cine Divas

> **Duração:** uns 8 a 10 minutos.
> **Como usar:** cada parte tem **📺 O que mostrar na tela** e **🎤 O que falar**. Não precisa decorar palavra por palavra:
> leia algumas vezes, entenda a ideia e fale do seu jeito. 💗

---

## ✅ Antes de gravar (checklist)

- [ ] Abrir o terminal na pasta do projeto e ativar o ambiente virtual.
- [ ] Rodar o site: `python run.py` e abrir **http://127.0.0.1:5000**.
- [ ] Ter uma conta já criada (ou criar uma ao vivo na Parte 2).
- [ ] Deixar estes arquivos **já abertos em abas** no VS Code, nesta ordem:
  1. `app/db.py`
  2. `app/__init__.py`
  3. `run.py`
  4. `app/models/filme.py`
  5. `app/controllers/filmes_controller.py`
  6. `views/filme_form.html`
  7. `views/filmes.html`
  8. `app/models/usuario.py`
- [ ] Aumentar o zoom do VS Code (Ctrl + `+`) para o código ficar legível no vídeo.
- [ ] Separar um filme para cadastrar ao vivo. Sugestão: **Diário de uma Paixão**, 2004, mood "Para chorar".

---

## 1️⃣ Abertura (~30s)

📺 **Tela:** o site aberto na página de login.

🎤 **Fala:**
> "Oi! Eu sou a Alice e esse é o **Cine Divas**, um site de filmes de romance com visual anos 2000, feito em **Flask**
> com banco de dados **SQLite**. Ele tem cadastro e login de usuárias e um **CRUD de filmes**: dá para cadastrar,
> listar, editar e excluir. Primeiro vou mostrar o site funcionando e depois explicar o código, principalmente
> a parte do banco de dados."

---

## 2️⃣ Demonstração do site (~1min30)

📺 **Tela:** o navegador. Vá fazendo enquanto fala.

1. **Login:** mostre a caixa "Você tem cadastro?", entre com a sua conta.
   > "Aqui é o login. Se a pessoa não tem conta, clica aqui e vai para o cadastro. O e-mail é o login."
2. **Listagem:** role a página dos filmes.
   > "Essa é a listagem. Todos esses filmes estão vindo do banco de dados, não de uma lista no código."
3. **Cadastrar:** clique em **+ cadastrar filme**, preencha e clique em **salvar ♡**.
   > "Vou cadastrar um filme novo... clico em salvar... e ele já aparece aqui no final da lista."
4. **Editar:** abra o filme novo, clique em **editar**, mude o mood e salve.
   > "Posso editar: mudo o mood, salvo, e a alteração foi gravada."
5. **Excluir:** clique em **excluir** e confirme.
   > "E posso excluir. Pronto, ele sumiu da lista e do banco."

---

## 3️⃣ Como o projeto é organizado (~1min)

📺 **Tela:** o explorador de arquivos do VS Code, mostrando as pastas.

🎤 **Fala:**
> "O projeto é dividido assim:
> - o **`db.py`** cuida do banco: é a única conexão do projeto e é onde as tabelas são criadas;
> - na pasta **`models`** ficam as **classes**: `Filme` e `Usuario`. Cada classe tem o SQL da sua tabela;
> - na pasta **`controllers`** ficam as **rotas**, que recebem o formulário e chamam a classe. As rotas não têm SQL;
> - na pasta **`views`** ficam as páginas HTML.
>
> O caminho é sempre esse: **a rota chama a classe, a classe usa a conexão do `db.py`, e o dado vai para o arquivo do banco.**"

💡 Se quiser, mostre este desenho (pode estar num slide ou só falar):
```
rota (controller)  →  classe (Filme / Usuario)  →  get_db() do db.py  →  arquivo .db
```

---

## 4️⃣ O banco de dados: `db.py` (~2min)

📺 **Tela:** `app/db.py`.

**Linhas 10 a 27, o `SCHEMA`:**
> "Aqui está a estrutura do banco. É **um banco só**, com **duas tabelas**: `usuarios` e `filmes`.
> O `CREATE TABLE IF NOT EXISTS` só cria a tabela se ela ainda não existir.
> O `id` é `AUTOINCREMENT`, então o banco gera o número sozinho.
> O `email` é `UNIQUE`, então o banco não deixa dois cadastros com o mesmo e-mail.
> E a senha é guardada como `senha_hash`, embaralhada, nunca a senha de verdade."

**Linha 35, os `FILMES_INICIAIS`:**
> "Esses são os 10 filmes iniciais. Eles só servem para **encher o banco na primeira vez**, quando a tabela está vazia.
> A tela nunca lê essa lista, ela sempre lê do banco."

**Linhas 93 a 105, `get_db()` e `close_db()`:**
> "O `get_db()` é a **única conexão do projeto**. Ele abre o banco com `sqlite3.connect` e guarda no `g`, que dura
> uma requisição. Se for chamado de novo na mesma requisição, reaproveita a mesma conexão.
> O `close_db()` fecha a conexão no fim de cada requisição. O Flask chama ele sozinho."

**Linhas 112 a 127, `init_app()`:**
> "O `init_app()` prepara o banco: executa o `SCHEMA` para criar as tabelas, conta quantos filmes tem
> e, se for zero, insere os filmes iniciais com o `executemany`. No fim faz o `commit` para gravar."

---

## 5️⃣ Por que as tabelas são criadas uma vez só (~1min)

📺 **Tela:** `app/__init__.py` na **linha 42**, depois `run.py`.

🎤 **Fala:**
> "O `init_app()` é chamado num lugar só: aqui no `create_app()`, quando o site abre."

(troque para o `run.py`)

> "E aqui tem um detalhe importante: o `use_reloader=False`. Quando o Flask roda com `debug=True`, ele liga um
> recarregador automático que **abre o programa duas vezes**, e as tabelas seriam criadas duas vezes.
> Desligando o reloader, o site abre uma vez só e as tabelas são criadas **uma única vez**.
> E mesmo se rodasse de novo, o `IF NOT EXISTS` e o `if total == 0` garantem que nada duplica."

---

## 6️⃣ A classe `Filme` (~2min)

📺 **Tela:** `app/models/filme.py`.

**Linha 1:**
> "A classe importa o `get_db`, então ela usa a **mesma conexão** do resto do projeto."

**Linha 7, `__init__`:**
> "O construtor guarda os dados do filme no objeto. Um filme novo começa com `id = None`, porque ainda não está no banco."

**Linhas 16 a 33, `salvar()`:**
> "O `salvar()` faz duas coisas. Se o filme **não tem id**, é novo, então faz um `INSERT`.
> Se **já tem id**, é uma edição, então faz um `UPDATE` com `WHERE id`.
> Os pontos de interrogação são preenchidos pelo `sqlite3` com os valores. Isso **protege contra SQL Injection**.
> Depois do `INSERT`, o `cursor.lastrowid` pega o id que o banco gerou.
> E o `commit`, na linha 33, é o que **grava de verdade** no arquivo."

**Linha 35, `excluir()`:**
> "O `excluir()` faz um `DELETE` pelo id e dá `commit`."

**Linhas 41 e 49, `listar()` e `buscar_por_id()`:**
> "O `listar()` faz um `SELECT` de todos os filmes, com um filtro de busca pelo título, e transforma cada linha do banco
> num objeto `Filme`. O `buscar_por_id()` busca um filme só. Se não achar, devolve `None` e a página mostra erro 404."

---

## 7️⃣ O caminho do dado, do botão até a tela (~2min) ⭐ PARTE MAIS IMPORTANTE

📺 **Tela:** vá trocando de arquivo conforme fala.

**1. `views/filme_form.html`, linhas 17 e 41:**
> "Tudo começa aqui no formulário. Quando eu clico em **salvar**, o navegador envia um `POST` com os dados
> do filme para a rota `/filmes/novo`."

**2. `app/controllers/filmes_controller.py`, linhas 60 a 69:**
> "A rota `novo()` recebe esse POST. Ela usa o `ler_formulario()` para pegar os campos e validar.
> Depois, na linha 67, cria o objeto: `filme = Filme(**dados)`. E chama `filme.salvar()`.
> Repara que **aqui não tem nenhum SQL**: a rota só usa a classe."

**3. `app/models/filme.py`, linhas 16 a 33:**
> "O `salvar()` pega a conexão com o `get_db()`, como o filme não tem id faz o `INSERT`, e dá `commit`.
> Nesse momento o filme está gravado no arquivo `.db`."

**4. Volta no controller (linha 69 em diante):**
> "A rota mostra a mensagem 'Filme cadastrado!' e redireciona para a listagem."

**5. Controller, linha 47, e depois `views/filmes.html`, linha 25:**
> "A listagem chama o `Filme.listar()`, que faz o `SELECT` no banco. O resultado vai para o HTML, e aqui
> o `{% for filme in filmes %}` do Jinja mostra cada filme na tela. Por isso o filme novo aparece na hora."

**6. Fechando:**
> "E no fim da requisição, o Flask chama o `close_db()` e a conexão é fechada."

---

## 8️⃣ Login e usuárias, rapidinho (~40s)

📺 **Tela:** `app/models/usuario.py`.

🎤 **Fala:**
> "A classe `Usuario` segue o mesmo padrão. O `salvar()` faz o `INSERT` da usuária e o `buscar_por_email()` é usado
> no login. Antes de salvar, a senha passa pelo `generate_password_hash`, e no login o `check_password_hash` compara.
> Então a senha **nunca** fica salva em texto puro."

---

## 9️⃣ Testes (~40s)

📺 **Tela:** o terminal. Pare o servidor (Ctrl+C) e rode:
```bash
python -m unittest -v
```

🎤 **Fala:**
> "Eu também tenho testes automáticos. Eles usam um banco temporário, então não mexem nos dados reais.
> Eles testam o cadastro, o login, a listagem, cadastrar, editar e excluir filme, a busca, e que os filmes
> iniciais não duplicam. Como dá para ver, os 13 testes passaram."

---

## 🔟 Encerramento (~20s)

📺 **Tela:** volte para o site.

🎤 **Fala:**
> "Resumindo: um banco só, criado uma única vez quando o site abre; cada tabela tem uma classe com o seu SQL;
> as rotas não têm SQL; e tudo usa só o `sqlite3`, sem ORM. Esse foi o Cine Divas, obrigada! 💗"

---

## 🆘 Se travar ou esquecer

Respira e volte para estas **4 frases**, que explicam o projeto inteiro:

1. "**Um banco só**, com duas tabelas, criado **uma vez** quando o site abre."
2. "**Cada tabela tem uma classe** com o seu SQL: `Filme` e `Usuario`."
3. "**A rota não tem SQL**: ela lê o formulário, cria o objeto e chama o método."
4. "O **`?`** protege contra SQL Injection e o **`commit`** grava no arquivo."

## 📌 Cola rápida de palavras

| Palavra | Quer dizer |
|---|---|
| `sqlite3` | biblioteca do Python para usar o banco SQLite (sem ORM) |
| `get_db()` | a única conexão com o banco |
| `close_db()` | fecha a conexão no fim da requisição |
| `init_app()` | cria as tabelas e os filmes iniciais (uma vez) |
| `execute` | roda **um** comando SQL |
| `executescript` | roda **vários** comandos SQL de uma vez |
| `executemany` | roda o mesmo comando para **vários** valores |
| `commit()` | grava de verdade no arquivo |
| `fetchone()` / `fetchall()` | pega uma linha / todas as linhas do resultado |
| `lastrowid` | o id que o banco acabou de gerar |
| `?` | espaço para o valor, protege contra SQL Injection |
| `self` | o próprio objeto (um filme específico) |
| `cls` / `@classmethod` | a classe; usado quando ainda não existe um objeto (listar, buscar) |
| `POST` | o formulário enviando dados para o servidor |
| `{% for %}` | o Jinja repetindo o HTML para cada filme |

> 💡 **Dica de gravação:** pode gravar em partes (uma parte de cada vez) e juntar depois. Fica bem mais fácil
> do que fazer os 10 minutos de uma vez só.
