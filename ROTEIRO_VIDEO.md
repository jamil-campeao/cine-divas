# 🎬 Roteiro do vídeo — Projeto Final Cine Divas (máximo 5 minutos)

> Cada parte tem **📺 o que mostrar** e **🎤 o que falar**. Não precisa decorar: entenda a ideia e fale do seu jeito.
> O tempo é curto, então **fale direto e não pare para explicar linha por linha**. 💗

## ✅ Antes de gravar
- [ ] `python iniciar_bd.py` e `python run.py` rodando, terminal visível (para mostrar os logs).
- [ ] Ter **saído** do site antes (para mostrar o cookie preenchendo o e-mail).
- [ ] Abas abertas no VS Code: `app/db.py`, `iniciar_bd.py`, `app/models/filme.py`,
      `app/controllers/filmes_controller.py`, `app/utils/auth_middleware.py`, `app/__init__.py`.
- [ ] Zoom do VS Code aumentado (Ctrl + `+`).

---

## 1️⃣ Abertura — 0:00 a 0:15
🎤 > "Oi, eu sou a Alice. Esse é o **Cine Divas**, um catálogo de filmes de romance com avaliações, feito em
> Flask, Jinja2 e SQLite, seguindo o padrão MVC."

## 2️⃣ Demonstração — 0:15 a 1:45
📺 Vá fazendo no navegador enquanto fala:
1. Tente abrir `/filmes` sem login → volta para o login com mensagem.
   > "As rotas são protegidas pelo middleware: sem login, volta pra cá."
2. Mostre o e-mail **já preenchido**.
   > "Esse e-mail veio de um **cookie** que guardei no último login."
3. Erre a senha → flash vermelho. Depois entre certo.
   > "Senha errada mostra uma flash message de erro."
4. **Filmes:** cadastre um com o ano "abc" (erro de validação), corrija e salve. Use a busca. Exclua.
   > "Primeiro gerenciamento: filmes. Tem cadastro com validação, listagem com busca, edição e exclusão."
5. **Avaliações:** abra um filme, dê 5 estrelas, vá em "avaliações", exclua.
   > "Segundo gerenciamento: avaliações, ligadas ao filme."
6. Abra `/filmes/999`.
   > "E uma página 404 personalizada."
7. Mostre o terminal.
   > "Aqui os **logs**: login, cadastro, exclusão..."

## 3️⃣ Estrutura MVC — 1:45 a 2:05
📺 Explorador de arquivos.
🎤 > "Models com as classes e o SQL, views com os templates que herdam do `base.html`, controllers com os
> blueprints, que **não têm SQL**, e o middleware na pasta `utils`."

## 4️⃣ `DatabaseConnection` — 2:05 a 2:40
📺 `app/db.py`.
🎤 > "Essa é a classe do padrão da Aula 15. Ela é usada com `with`. No `__enter__` ela abre o banco, cria o cursor
> e ativa as chaves estrangeiras. No `__exit__`, se deu certo faz `commit`, se deu erro faz `rollback`, e
> sempre fecha a conexão."

## 5️⃣ `iniciar_bd.py` — 2:40 a 3:00
📺 `iniciar_bd.py`.
🎤 > "Esse script cria as três tabelas com chave primária e chave estrangeira com `ON DELETE CASCADE`: se apagar
> um filme, as avaliações dele vão junto. E cria a usuária de teste usando o `salvar()` da classe `Usuario`."

## 6️⃣ Model — 3:00 a 3:35
📺 `app/models/filme.py`.
🎤 > "Cada método abre a conexão com `with DatabaseConnection()`. O SQL usa sempre `?`, que evita SQL Injection,
> e **todo** comando filtra por `usuario_id`, então uma usuária não vê nem apaga o filme de outra."

## 7️⃣ Controller — 3:35 a 4:00
📺 `app/controllers/filmes_controller.py`, rota `novo()`.
🎤 > "A rota lê o formulário, valida, cria o objeto `Filme` e chama o `salvar()`. Depois dá `flash` e
> `redirect`. Nenhum SQL aqui."

## 8️⃣ Middleware — 4:00 a 4:25
📺 `app/utils/auth_middleware.py`.
🎤 > "O `@login_required` pega o `user_id` da sessão, **confere no banco** se a usuária existe e guarda em
> `g.usuario`. Se não existir, manda pro login."

## 9️⃣ Adaptações — 4:25 a 4:50
🎤 > "Duas adaptações em relação ao padrão das aulas: no `session['username']` eu guardo o **nome**, porque o
> login é por e-mail e não existe campo username. E o caminho do banco aceita uma variável de ambiente para
> os testes automáticos usarem um banco separado."

## 🔟 Fim — 4:50 a 5:00
🎤 > "Esse foi o Cine Divas. Obrigada! 💗"

---

## 🆘 Se travar
1. "**DatabaseConnection** com `with`: commit se der certo, rollback se der erro, e fecha."
2. "**SQL só nos Models**, sempre com `?` e filtrando por `usuario_id`."
3. "**Controller** não tem SQL: lê, valida, chama o Model e redireciona."
4. "**Middleware** confere a usuária no banco e guarda em `g.usuario`."

> 💡 Grave por partes e junte depois. Cronometre: se passar de 5 minutos, corte a demonstração (parte 2) primeiro.
