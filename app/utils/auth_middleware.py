from functools import wraps

from flask import flash, g, redirect, session, url_for

from app.models.usuario import Usuario


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        g.usuario = Usuario.buscar_por_id(user_id) if user_id else None

        if g.usuario is None:
            session.clear()
            flash("Faça login pra ver os filmes, diva! ♡", "erro")
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapper
