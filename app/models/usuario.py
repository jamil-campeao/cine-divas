from app.db import DatabaseConnection


class Usuario:
    def __init__(self, nome, email, senha_hash, id=None, criado_em=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.criado_em = criado_em

    def salvar(self):
        # Se o e-mail já existir, o banco lança sqlite3.IntegrityError (coluna UNIQUE).
        with DatabaseConnection() as db:
            db.cursor.execute(
                "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                (self.nome, self.email, self.senha_hash),
            )
            self.id = db.cursor.lastrowid

    @classmethod
    def buscar_por_id(cls, id):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
            linha = db.cursor.fetchone()
        return cls(**dict(linha)) if linha else None

    @classmethod
    def buscar_por_email(cls, email):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            linha = db.cursor.fetchone()
        return cls(**dict(linha)) if linha else None
