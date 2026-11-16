from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, session, url_for

from app.models.avaliacao import Avaliacao
from app.models.filme import Filme
from app.utils.auth_middleware import login_required

filmes_bp = Blueprint("filmes", __name__)


def ler_formulario():
    """Pega os campos do formulário e valida. Devolve (dados, erro)."""
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
    if len(dados["titulo"]) > 100 or len(dados["mood"]) > 40 or len(dados["sinopse"]) > 1000:
        return dados, "Título até 100, mood até 40 e sinopse até 1000 caracteres."
    if not dados["ano"].isdigit() or not 1900 <= int(dados["ano"]) <= 2100:
        return dados, "O ano precisa ser um número entre 1900 e 2100."
    dados["ano"] = int(dados["ano"])
    return dados, None


def buscar_ou_404(id):
    filme = Filme.buscar_por_id(id, g.usuario.id)
    if filme is None:
        abort(404)
    return filme


@filmes_bp.route("/")
def inicio():
    if session.get("user_id"):
        return redirect(url_for("filmes.lista"))
    return redirect(url_for("auth.login"))


@filmes_bp.route("/filmes")
@login_required
def lista():
    busca = request.args.get("busca", "").strip()
    filmes = Filme.listar_por_usuario(g.usuario.id, busca)
    return render_template("filmes.html", filmes=filmes, busca=busca)


@filmes_bp.route("/filmes/<int:id>")
@login_required
def detalhe(id):
    filme = buscar_ou_404(id)
    avaliacoes = Avaliacao.listar_por_filme(id, g.usuario.id)
    return render_template("filme.html", filme=filme, avaliacoes=avaliacoes)


@filmes_bp.route("/filmes/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        dados, erro = ler_formulario()
        if erro:
            flash(erro, "erro")
            return render_template("filme_form.html", filme=dados, titulo_pagina="novo filme")

        filme = Filme(**dados, usuario_id=g.usuario.id)
        filme.salvar()
        current_app.logger.info("Filme cadastrado: %s (usuária %s)", filme.titulo, g.usuario.id)
        flash("Filme cadastrado! 💗", "sucesso")
        return redirect(url_for("filmes.lista"))

    return render_template("filme_form.html", filme={}, titulo_pagina="novo filme")


@filmes_bp.route("/filmes/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    filme = buscar_ou_404(id)

    if request.method == "POST":
        dados, erro = ler_formulario()
        if erro:
            flash(erro, "erro")
            return render_template("filme_form.html", filme=dados, titulo_pagina="editar filme")

        Filme(**dados, usuario_id=g.usuario.id, id=id).atualizar()
        flash("Filme atualizado! ✧", "sucesso")
        return redirect(url_for("filmes.detalhe", id=id))

    return render_template("filme_form.html", filme=filme, titulo_pagina="editar filme")


@filmes_bp.route("/filmes/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):
    filme = buscar_ou_404(id)
    filme.excluir()
    current_app.logger.info("Filme excluído: %s (usuária %s)", filme.titulo, g.usuario.id)
    flash("Filme excluído. 💔", "sucesso")
    return redirect(url_for("filmes.lista"))
