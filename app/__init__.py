import os

from flask import Flask

from app import db

# Raiz do projeto (pasta que contém app/, views/ e static/).
# Caminhos absolutos garantem que o CSS e os templates sejam encontrados
# não importa de qual pasta o `python run.py` for executado.
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(RAIZ, "views"),
        static_folder=os.path.join(RAIZ, "static"),
        static_url_path="/static",
        instance_path=os.path.join(RAIZ, "instance"),
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "cine-divas-chave-local")
    app.config["DATABASE"] = os.path.join(app.instance_path, "cine_divas.db")
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    from app.models.filme import Filme

    with app.app_context():
        Filme.criar_tabela()

    from app.controllers.auth_controller import auth
    from app.controllers.filmes_controller import filmes

    app.register_blueprint(auth)
    app.register_blueprint(filmes)

    return app
