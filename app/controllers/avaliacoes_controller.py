from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for

from app.models.avaliacao import Avaliacao
from app.models.filme import Filme
from app.utils.auth_middleware import login_required

avaliacoes_bp = Blueprint("avaliacoes", __name__)


@avaliacoes_bp.route("/avaliacoes")
@login_required
def lista():
    avaliacoes = Avaliacao.listar_por_usuario(g.usuario.id)
    return render_template("avaliacoes.html", avaliacoes=avaliacoes)


@avaliacoes_bp.route("/filmes/<int:filme_id>/avaliacoes", methods=["POST"])
@login_required
def nova(filme_id):
    if Filme.buscar_por_id(filme_id, g.usuario.id) is None:
        abort(404)

    nota = request.form.get("nota", "").strip()
    comentario = request.form.get("comentario", "").strip()

    if not nota.isdigit() or not 1 <= int(nota) <= 5:
        flash("Escolha uma nota de 1 a 5.", "erro")
    elif len(comentario) > 500:
        flash("O comentário pode ter no máximo 500 caracteres.", "erro")
    else:
        Avaliacao(int(nota), comentario, filme_id, g.usuario.id).salvar()
        current_app.logger.info("Avaliação criada no filme %s (usuária %s)", filme_id, g.usuario.id)
        flash("Avaliação salva! ⭐", "sucesso")

    return redirect(url_for("filmes.detalhe", id=filme_id))


@avaliacoes_bp.route("/avaliacoes/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):
    avaliacao = Avaliacao.buscar_por_id(id, g.usuario.id)
    if avaliacao is None:
        abort(404)

    avaliacao.excluir()
    current_app.logger.info("Avaliação %s excluída (usuária %s)", id, g.usuario.id)
    flash("Avaliação excluída. 💔", "sucesso")
    return redirect(url_for("filmes.detalhe", id=avaliacao.filme_id))
