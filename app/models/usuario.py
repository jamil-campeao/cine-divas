from app.db import get_db


class Usuario:
    """Uma usuária. Todo o SQL da tabela `usuarios` fica nesta classe."""

    def __init__(self, nome, email, senha_hash, id=None, criado_em=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.criado_em = criado_em

    def salvar(self):
        """Grava uma usuária nova. Se o e-mail já existir, o banco lança sqlite3.IntegrityError."""
        conexao = get_db()
        cursor = conexao.execute(
            "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
            (self.nome, self.email, self.senha_hash),
        )
        self.id = cursor.lastrowid
        conexao.commit()

    @classmethod
    def buscar_por_email(cls, email):
        """Devolve a Usuario com esse e-mail, ou None se não existir."""
        linha = get_db().execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        return cls(**dict(linha)) if linha else None
