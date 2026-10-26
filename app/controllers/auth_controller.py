import re
import sqlite3
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

auth = Blueprint("auth", __name__)

EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def login_obrigatorio(view):
    """Redireciona para o login quando não há usuária na sessão."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login pra ver os filmes, diva! ♡", "erro")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapper


@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")

        if not nome or not email or not senha or not confirmar:
            flash("Preencha todos os campos.", "erro")
        elif not EMAIL_VALIDO.match(email):
            flash("Esse e-mail não parece válido.", "erro")
        elif len(senha) < 6:
            flash("A senha precisa ter pelo menos 6 caracteres.", "erro")
        elif senha != confirmar:
            flash("As senhas não são iguais.", "erro")
        else:
            try:
                conexao = get_db()
                conexao.execute(
                    "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                    (nome, email, generate_password_hash(senha)),
                )
                conexao.commit()
                flash("Conta criada! Agora é só entrar 💗", "sucesso")
                return redirect(url_for("auth.login"))
            except sqlite3.IntegrityError:
                flash("Já existe uma conta com esse e-mail.", "erro")

        return render_template("cadastro.html", nome=nome, email=email)

    return render_template("cadastro.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        return redirect(url_for("filmes.lista"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()

        if usuario and check_password_hash(usuario["senha_hash"], senha):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]
            return redirect(url_for("filmes.lista"))

        flash("E-mail ou senha incorretos.", "erro")
        return render_template("login.html", email=email)

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    flash("Até a próxima sessão de cinema! 💋", "sucesso")
    return redirect(url_for("auth.login"))
