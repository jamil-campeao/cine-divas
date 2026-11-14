
import os

from flask import Flask

from app import db


# Raiz do projeto
RAIZ = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


def create_app(config=None):

    app = Flask(
        __name__,
        template_folder=os.path.join(RAIZ, "views"),
        static_folder=os.path.join(RAIZ, "static"),
        static_url_path="/static",
        instance_path=os.path.join(RAIZ, "instance"),
    )

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "cine-divas-chave-local"
    )

    app.config["DATABASE"] = os.path.join(
        app.instance_path,
        "cine_divas.db"
    )

    # Permite trocar configurações (os testes usam um banco temporário).
    if config:
        app.config.update(config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Cria as tabelas uma única vez, quando o site abre.
    db.init_app(app)

    # Importa os controllers.
    from app.controllers.auth_controller import auth
    from app.controllers.filmes_controller import filmes

    # Registra as rotas.
    app.register_blueprint(auth)
    app.register_blueprint(filmes)

    return app
