import sqlite3

from app.db import (
    inserir_filme,
    atualizar_filme,
    excluir_filme,
    listar_filmes,
    buscar_filme_por_id
)


# =====================================================================
# CLASSE FILME
# Representa UM filme (título, ano, mood...) e também guarda TODO o
# SQL da tabela "filmes". As rotas não escrevem SQL: elas só criam um
# Filme e chamam os métodos daqui (salvar, excluir, listar...).
# =====================================================================
class Filme:
    """Representa um filme e organiza seus dados."""

    def __init__(self, titulo, ano, mood, sinopse,
                 emoji="🎬", poster="", id=None):

        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.mood = mood
        self.sinopse = sinopse
        self.emoji = emoji
        self.poster = poster

    def salvar(self):
        """Insere um filme novo ou atualiza um filme existente."""

        dados = {
            "titulo": self.titulo,
            "ano": self.ano,
            "mood": self.mood,
            "sinopse": self.sinopse,
            "emoji": self.emoji,
            "poster": self.poster
        }

        if self.id is None:
            self.id = inserir_filme(dados)
        else:
            atualizar_filme(self.id, dados)

    # -----------------------------------------------------------------
    # excluir()  ->  DELETE
    # Apaga ESTE filme do banco, usando o id dele.
    # -----------------------------------------------------------------
    def excluir(self):
        """Exclui o filme do banco de dados."""

        excluir_filme(self.id)

    @classmethod
    def listar(cls, busca=""):
        """Retorna os filmes encontrados no banco."""

        linhas = listar_filmes(busca)

        return [
            cls(**dict(linha))
            for linha in linhas
        ]

    # -----------------------------------------------------------------
    # buscar_por_id()  ->  READ (um)
    # Busca UM filme pelo id. Usado no detalhe, na edição e na exclusão.
    # Devolve o objeto Filme, ou None se não achar (aí a rota mostra 404).
    # -----------------------------------------------------------------
    @classmethod
    def buscar_por_id(cls, id):
        """Busca um filme pelo identificador."""

        linha = buscar_filme_por_id(id)

        return cls(**dict(linha)) if linha else None
