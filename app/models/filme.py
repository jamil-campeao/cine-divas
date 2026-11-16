from app.db import DatabaseConnection


class Filme:
    def __init__(self, titulo, ano, mood, sinopse, emoji="🎬", poster="", usuario_id=None, id=None):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.mood = mood
        self.sinopse = sinopse
        self.emoji = emoji
        self.poster = poster
        self.usuario_id = usuario_id

    def salvar(self):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "INSERT INTO filmes (titulo, ano, mood, sinopse, emoji, poster, usuario_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.titulo, self.ano, self.mood, self.sinopse, self.emoji, self.poster, self.usuario_id),
            )
            self.id = db.cursor.lastrowid

    def atualizar(self):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "UPDATE filmes SET titulo = ?, ano = ?, mood = ?, sinopse = ?, emoji = ?, poster = ? "
                "WHERE id = ? AND usuario_id = ?",
                (self.titulo, self.ano, self.mood, self.sinopse, self.emoji, self.poster, self.id, self.usuario_id),
            )

    def excluir(self):
        # As avaliações do filme somem junto (ON DELETE CASCADE).
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM filmes WHERE id = ? AND usuario_id = ?", (self.id, self.usuario_id))

    @classmethod
    def listar_por_usuario(cls, usuario_id, busca=""):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT * FROM filmes WHERE usuario_id = ? AND titulo LIKE '%' || ? || '%' ORDER BY id",
                (usuario_id, busca),
            )
            linhas = db.cursor.fetchall()
        return [cls(**dict(linha)) for linha in linhas]

    @classmethod
    def buscar_por_id(cls, id, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM filmes WHERE id = ? AND usuario_id = ?", (id, usuario_id))
            linha = db.cursor.fetchone()
        return cls(**dict(linha)) if linha else None
