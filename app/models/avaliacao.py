from app.db import DatabaseConnection


class Avaliacao:
    def __init__(self, nota, comentario, filme_id, usuario_id, id=None, criado_em=None, filme_titulo=None):
        self.id = id
        self.nota = nota
        self.comentario = comentario
        self.filme_id = filme_id
        self.usuario_id = usuario_id
        self.criado_em = criado_em
        self.filme_titulo = filme_titulo  # vem do JOIN com filmes

    def salvar(self):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "INSERT INTO avaliacoes (nota, comentario, filme_id, usuario_id) VALUES (?, ?, ?, ?)",
                (self.nota, self.comentario, self.filme_id, self.usuario_id),
            )
            self.id = db.cursor.lastrowid

    def excluir(self):
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM avaliacoes WHERE id = ? AND usuario_id = ?", (self.id, self.usuario_id))

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT avaliacoes.*, filmes.titulo AS filme_titulo FROM avaliacoes "
                "JOIN filmes ON filmes.id = avaliacoes.filme_id "
                "WHERE avaliacoes.usuario_id = ? ORDER BY avaliacoes.id DESC",
                (usuario_id,),
            )
            linhas = db.cursor.fetchall()
        return [cls(**dict(linha)) for linha in linhas]

    @classmethod
    def listar_por_filme(cls, filme_id, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT * FROM avaliacoes WHERE filme_id = ? AND usuario_id = ? ORDER BY id DESC",
                (filme_id, usuario_id),
            )
            linhas = db.cursor.fetchall()
        return [cls(**dict(linha)) for linha in linhas]

    @classmethod
    def buscar_por_id(cls, id, usuario_id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM avaliacoes WHERE id = ? AND usuario_id = ?", (id, usuario_id))
            linha = db.cursor.fetchone()
        return cls(**dict(linha)) if linha else None
