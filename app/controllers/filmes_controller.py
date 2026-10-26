from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.controllers.auth_controller import login_obrigatorio
from app.models.filme import Filme

filmes = Blueprint("filmes", __name__)


def ler_formulario():
    """Pega os campos do formulário HTML e valida. Retorna (dados, erro)."""
    dados = {
        "titulo": request.form.get("titulo", "").strip(),
        "ano": request.form.get("ano", "").strip(),
        "mood": request.form.get("mood", "").strip(),
        "sinopse": request.form.get("sinopse", "").strip(),
        "emoji": request.form.get("emoji", "").strip() or "🎬",
        "poster": request.form.get("poster", "").strip(),
    }
    if not dados["titulo"] or not dados["ano"] or not dados["mood"] or not dados["sinopse"]:
        return dados, "Preencha título, ano, mood e sinopse."
    if not dados["ano"].isdigit():
        return dados, "O ano precisa ser um número."
    dados["ano"] = int(dados["ano"])
    return dados, None


def buscar_ou_404(id):
    filme = Filme.buscar_por_id(id)
    if filme is None:
        abort(404)
    return filme


@filmes.route("/")
def inicio():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("filmes.lista"))


# ---------- Read: listagem e detalhe ----------

@filmes.route("/filmes")
@login_obrigatorio
def lista():
    busca = request.args.get("busca", "").strip()
    return render_template("filmes.html", filmes=Filme.listar(busca), busca=busca)


@filmes.route("/filmes/<int:id>")
@login_obrigatorio
def detalhe(id):
    return render_template("filme.html", filme=buscar_ou_404(id))


# ---------- Create ----------

@filmes.route("/filmes/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo():
    if request.method == "POST":
        dados, erro = ler_formulario()
        if erro:
            flash(erro, "erro")
            return render_template("filme_form.html", filme=dados, titulo_pagina="novo filme")

        filme = Filme(**dados)  # 1) crio o objeto com os dados do formulário
        filme.salvar()          # 2) a classe faz o INSERT no banco
        flash("Filme cadastrado! 💗", "sucesso")
        return redirect(url_for("filmes.lista"))

    return render_template("filme_form.html", filme={}, titulo_pagina="novo filme")


# ---------- Update ----------

@filmes.route("/filmes/<int:id>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar(id):
    filme = buscar_ou_404(id)

    if request.method == "POST":
        dados, erro = ler_formulario()
        if erro:
            flash(erro, "erro")
            return render_template("filme_form.html", filme=dados, titulo_pagina="editar filme")

        filme = Filme(id=id, **dados)  # com id, salvar() faz UPDATE
        filme.salvar()
        flash("Filme atualizado! ✧", "sucesso")
        return redirect(url_for("filmes.detalhe", id=id))

    return render_template("filme_form.html", filme=filme, titulo_pagina="editar filme")


# ---------- Delete ----------

@filmes.route("/filmes/<int:id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir(id):
    buscar_ou_404(id).excluir()
    flash("Filme excluído. 💔", "sucesso")
    return redirect(url_for("filmes.lista"))
