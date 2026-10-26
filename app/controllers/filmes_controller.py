from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from app.controllers.auth_controller import login_obrigatorio
from app.filmes import FILMES, buscar_filme

filmes = Blueprint("filmes", __name__)


@filmes.route("/")
def inicio():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    return redirect(url_for("filmes.lista"))


@filmes.route("/filmes")
@login_obrigatorio
def lista():
    busca = request.args.get("busca", "").strip()
    resultado = FILMES
    if busca:
        resultado = [f for f in FILMES if busca.casefold() in f["titulo"].casefold()]
    return render_template("filmes.html", filmes=resultado, total=len(FILMES), busca=busca)


@filmes.route("/filmes/<slug>")
@login_obrigatorio
def detalhe(slug):
    filme = buscar_filme(slug)
    if filme is None:
        abort(404)
    numero = FILMES.index(filme) + 1
    return render_template("filme.html", filme=filme, numero=numero)
