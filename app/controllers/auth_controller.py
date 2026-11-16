import re
import sqlite3

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)

EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TRINTA_DIAS = 60 * 60 * 24 * 30


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")

        if not nome or not email or not senha or not confirmar:
            flash("Preencha todos os campos.", "erro")
        elif len(nome) > 60:
            flash("O nome pode ter no máximo 60 caracteres.", "erro")
        elif not EMAIL_VALIDO.match(email):
            flash("Esse e-mail não parece válido.", "erro")
        elif len(senha) < 6:
            flash("A senha precisa ter pelo menos 6 caracteres.", "erro")
        elif senha != confirmar:
            flash("As senhas não são iguais.", "erro")
        else:
            try:
                Usuario(nome, email, generate_password_hash(senha)).salvar()
                current_app.logger.info("Nova usuária cadastrada: %s", email)
                flash("Conta criada! Agora é só entrar 💗", "sucesso")
                return redirect(url_for("auth.login"))
            except sqlite3.IntegrityError:
                flash("Já existe uma conta com esse e-mail.", "erro")

        return render_template("cadastro.html", nome=nome, email=email)

    return render_template("cadastro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("filmes.lista"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = Usuario.buscar_por_email(email)

        if usuario and check_password_hash(usuario.senha_hash, senha):
            session.clear()
            session["user_id"] = usuario.id
            session["username"] = usuario.nome
            current_app.logger.info("Login realizado: %s", email)

            resposta = redirect(url_for("filmes.lista"))
            resposta.set_cookie("ultimo_email", email, max_age=TRINTA_DIAS)  # lembra o e-mail no próximo login
            return resposta

        current_app.logger.warning("Falha de login: %s", email)
        flash("E-mail ou senha incorretos.", "erro")
        return render_template("login.html", email=email)

    return render_template("login.html", email=request.cookies.get("ultimo_email", ""))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Até a próxima sessão de cinema! 💋", "sucesso")
    return redirect(url_for("auth.login"))
