import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    criado_em  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def init_app(app):
    with app.app_context():
        conexao = get_db()
        conexao.executescript(SCHEMA)
        conexao.commit()
        close_db()
    app.teardown_appcontext(close_db)
