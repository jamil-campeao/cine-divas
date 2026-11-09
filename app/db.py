# =====================================================================
# db.py
# Conexão com o banco usada pelo LOGIN e CADASTRO de usuárias
# (auth_controller.py). Também cria a tabela "usuarios".
# Os filmes NÃO usam este arquivo: a classe Filme tem o próprio conectar().
# =====================================================================

import sqlite3  # biblioteca do próprio Python para usar banco SQLite

from flask import current_app, g  # current_app = app rodando; g = "rascunho" que dura uma requisição

# ---------------------------------------------------------------------
# SCHEMA
# Texto com o SQL que cria a tabela de usuárias (se ainda não existir).
# Aqui ele é só um texto: quem executa é a init_app(), lá embaixo.
# - email UNIQUE: o banco não deixa dois cadastros com o mesmo e-mail.
# - senha_hash: guarda a senha embaralhada (hash), nunca a senha real.
# - criado_em: o banco preenche sozinho com a data/hora do cadastro.
# ---------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    criado_em  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


# ---------------------------------------------------------------------
# get_db()
# Entrega uma conexão com o banco.
# Na primeira vez dentro de uma requisição, abre a conexão e guarda no g.
# Se for chamada de novo na mesma requisição, reaproveita a mesma
# conexão em vez de abrir outra.
# ---------------------------------------------------------------------
def get_db():
    if "db" not in g:  # ainda não tem conexão aberta nesta requisição?
        g.db = sqlite3.connect(current_app.config["DATABASE"])  # abre o arquivo .db
        g.db.row_factory = sqlite3.Row  # deixa usar usuario["email"] em vez de usuario[2]
    return g.db


# ---------------------------------------------------------------------
# close_db()
# Fecha a conexão guardada no g, se existir.
# O Flask chama essa função sozinho no fim de toda requisição
# (isso é configurado na init_app). O "error" é passado pelo Flask;
# a gente não usa, mas o parâmetro precisa existir.
# ---------------------------------------------------------------------
def close_db(error=None):
    conexao = g.pop("db", None)  # tira a conexão do g (ou None se não tiver)
    if conexao is not None:
        conexao.close()


# ---------------------------------------------------------------------
# init_app()
# Roda UMA vez quando o site liga (chamada em app/__init__.py).
# 1) Cria a tabela "usuarios" executando o SCHEMA.
# 2) Avisa o Flask para chamar close_db() no fim de cada requisição.
# ---------------------------------------------------------------------
def init_app(app):
    with app.app_context():  # "liga" o app para poder usar current_app e g fora de uma requisição
        conexao = get_db()
        conexao.executescript(SCHEMA)  # executescript roda um texto com vários comandos SQL
        conexao.commit()  # confirma a criação da tabela
        close_db()
    app.teardown_appcontext(close_db)  # fecha a conexão sozinho no fim de toda requisição
