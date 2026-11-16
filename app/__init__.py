import logging
import os

from flask import Flask, render_template


def create_app():
    app = Flask(__name__, template_folder="views")
    app.secret_key = os.environ.get("SECRET_KEY", "cine-divas-chave-local")
    app.logger.setLevel(logging.INFO)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.avaliacoes_controller import avaliacoes_bp
    from app.controllers.filmes_controller import filmes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(filmes_bp)
    app.register_blueprint(avaliacoes_bp)

    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        return render_template("404.html"), 404

    return app
