from app.db import get_db


class Filme:
    """Um filme. Todo o SQL da tabela `filmes` fica nesta classe."""

    def __init__(self, titulo, ano, mood, sinopse, emoji="🎬", poster="", id=None):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.mood = mood
        self.sinopse = sinopse
        self.emoji = emoji
        self.poster = poster

    def salvar(self):
        """Sem id = filme novo (INSERT). Com id = edição (UPDATE)."""
        conexao = get_db()
        valores = (self.titulo, self.ano, self.mood, self.sinopse, self.emoji, self.poster)

        if self.id is None:
            cursor = conexao.execute(
                "INSERT INTO filmes (titulo, ano, mood, sinopse, emoji, poster) VALUES (?, ?, ?, ?, ?, ?)",
                valores,
            )
            self.id = cursor.lastrowid  # id gerado pelo banco
        else:
            conexao.execute(
                "UPDATE filmes SET titulo = ?, ano = ?, mood = ?, sinopse = ?, emoji = ?, poster = ? WHERE id = ?",
                valores + (self.id,),
            )

        conexao.commit()

    def excluir(self):
        conexao = get_db()
        conexao.execute("DELETE FROM filmes WHERE id = ?", (self.id,))
        conexao.commit()

    @classmethod
    def listar(cls, busca=""):
        """Devolve uma lista de objetos Filme (filtrando pelo título)."""
        linhas = get_db().execute(
            "SELECT * FROM filmes WHERE titulo LIKE ? ORDER BY id", (f"%{busca}%",)
        ).fetchall()
        return [cls(**dict(linha)) for linha in linhas]

    @classmethod
    def buscar_por_id(cls, id):
        """Devolve o Filme com esse id, ou None se não existir."""
        linha = get_db().execute("SELECT * FROM filmes WHERE id = ?", (id,)).fetchone()
        return cls(**dict(linha)) if linha else None
