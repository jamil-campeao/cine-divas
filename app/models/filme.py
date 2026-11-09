import sqlite3  # biblioteca do próprio Python para usar banco SQLite (sem ORM)

from flask import current_app  # o app Flask que está rodando; usado para pegar o caminho do banco


# =====================================================================
# CLASSE FILME
# Representa UM filme (título, ano, mood...) e também guarda TODO o
# SQL da tabela "filmes". As rotas não escrevem SQL: elas só criam um
# Filme e chamam os métodos daqui (salvar, excluir, listar...).
# =====================================================================
class Filme:

    # -----------------------------------------------------------------
    # __init__ (construtor)
    # Roda sozinho quando a gente escreve Filme(...).
    # Guarda os dados recebidos dentro do objeto (self).
    # Filme novo vem com id=None, porque ainda não está no banco.
    # -----------------------------------------------------------------
    def __init__(self, titulo, ano, mood, sinopse, emoji="🎬", poster="", id=None):
        self.id = id
        self.titulo = titulo
        self.ano = ano
        self.mood = mood
        self.sinopse = sinopse
        self.emoji = emoji
        self.poster = poster

    # -----------------------------------------------------------------
    # conectar()
    # Abre a conexão com o arquivo do banco (instance/cine_divas.db)
    # e devolve essa conexão para os outros métodos usarem.
    # @staticmethod = não precisa de um filme (self) nem da classe (cls).
    # -----------------------------------------------------------------
    @staticmethod
    def conectar():
        conexao = sqlite3.connect(current_app.config["DATABASE"])  # abre o arquivo .db
        conexao.row_factory = sqlite3.Row  # deixa usar linha["titulo"] em vez de linha[1]
        return conexao

    # -----------------------------------------------------------------
    # criar_tabela()
    # Roda uma vez quando o site liga (chamada em app/__init__.py).
    # 1) Cria a tabela "filmes" se ela ainda não existir.
    # 2) Conta quantos filmes tem. Se estiver vazia, grava os 10 iniciais.
    # @classmethod = recebe a classe (cls), não um filme específico.
    # -----------------------------------------------------------------
    @classmethod
    def criar_tabela(cls):
        conexao = cls.conectar()
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS filmes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo  TEXT NOT NULL,
                ano     INTEGER NOT NULL,
                mood    TEXT NOT NULL,
                sinopse TEXT NOT NULL,
                emoji   TEXT NOT NULL DEFAULT '🎬',
                poster  TEXT NOT NULL DEFAULT ''
            )
        """)
        total = conexao.execute("SELECT COUNT(*) FROM filmes").fetchone()[0]  # quantos filmes existem
        conexao.close()

        if total == 0:  # tabela vazia = primeira vez que o site roda
            for dados in FILMES_INICIAIS:
                cls(**dados).salvar()  # cria um Filme com o dicionário e grava no banco

    # -----------------------------------------------------------------
    # salvar()  ->  CREATE e UPDATE
    # Grava ESTE filme no banco.
    # - Se o filme não tem id: é novo, então faz INSERT (cadastro).
    # - Se o filme já tem id: já existe, então faz UPDATE (edição).
    # Os "?" são preenchidos pelo sqlite3 com os valores da tupla,
    # na mesma ordem (isso protege contra SQL Injection).
    # -----------------------------------------------------------------
    def salvar(self):
        conexao = self.conectar()
        if self.id is None:
            cursor = conexao.execute(
                "INSERT INTO filmes (titulo, ano, mood, sinopse, emoji, poster) VALUES (?, ?, ?, ?, ?, ?)",
                (self.titulo, self.ano, self.mood, self.sinopse, self.emoji, self.poster),
            )
            self.id = cursor.lastrowid  # pega o id que o banco acabou de gerar
        else:
            conexao.execute(
                "UPDATE filmes SET titulo = ?, ano = ?, mood = ?, sinopse = ?, emoji = ?, poster = ? WHERE id = ?",
                (self.titulo, self.ano, self.mood, self.sinopse, self.emoji, self.poster, self.id),
            )
        conexao.commit()  # confirma a gravação no arquivo (sem isso nada é salvo)
        conexao.close()

    # -----------------------------------------------------------------
    # excluir()  ->  DELETE
    # Apaga ESTE filme do banco, usando o id dele.
    # -----------------------------------------------------------------
    def excluir(self):
        conexao = self.conectar()
        conexao.execute("DELETE FROM filmes WHERE id = ?", (self.id,))  # a vírgula faz ser uma tupla
        conexao.commit()  # confirma a exclusão
        conexao.close()

    # -----------------------------------------------------------------
    # listar()  ->  READ (vários)
    # Busca os filmes no banco com SELECT e devolve uma LISTA de
    # objetos Filme. É essa lista que a página de filmes mostra com
    # {% for filme in filmes %}.
    # "busca" filtra pelo título: o % no LIKE significa "qualquer coisa".
    # -----------------------------------------------------------------
    @classmethod
    def listar(cls, busca=""):
        conexao = cls.conectar()
        linhas = conexao.execute(
            "SELECT * FROM filmes WHERE titulo LIKE ? ORDER BY id",
            (f"%{busca}%",),
        ).fetchall()  # pega todas as linhas do resultado
        conexao.close()
        return [cls(**dict(linha)) for linha in linhas]  # cada linha do banco vira um objeto Filme

    # -----------------------------------------------------------------
    # buscar_por_id()  ->  READ (um)
    # Busca UM filme pelo id. Usado no detalhe, na edição e na exclusão.
    # Devolve o objeto Filme, ou None se não achar (aí a rota mostra 404).
    # -----------------------------------------------------------------
    @classmethod
    def buscar_por_id(cls, id):
        conexao = cls.conectar()
        linha = conexao.execute("SELECT * FROM filmes WHERE id = ?", (id,)).fetchone()  # uma linha ou None
        conexao.close()
        return cls(**dict(linha)) if linha else None


# =====================================================================
# FILMES_INICIAIS
# Os 10 filmes que são gravados no banco UMA vez, pela criar_tabela(),
# quando a tabela está vazia. NÃO é usada para mostrar filmes na tela:
# a listagem sempre vem do SELECT em listar().
# =====================================================================
FILMES_INICIAIS = [
    {
        "titulo": "Como Perder um Homem em 10 Dias",
        "ano": 2003,
        "mood": "Para rir",
        "emoji": "💋",
        "poster": "img/como-perder-um-homem-em-10-dias.jpg",
        "sinopse": "Ela quer que ele termine com ela, e ele apostou que consegue fazê-la se "
                   "apaixonar. O resultado são duas pessoas se testando ao limite enquanto "
                   "tudo dá errado. É muito bom.",
    },
    {
        "titulo": "A Culpa é das Estrelas",
        "ano": 2014,
        "mood": "Para chorar",
        "emoji": "⭐",
        "poster": "img/a-culpa-e-das-estrelas.png",
        "sinopse": "A história de Hazel e Augustus em um grupo de apoio é bonita e dolorosa "
                   "na mesma medida. Um daqueles romances que marcam e que com certeza vão te "
                   "fazer chorar no final.",
    },
    {
        "titulo": "Minha Culpa",
        "ano": 2023,
        "mood": "Para viciar",
        "emoji": "🏎️",
        "poster": "img/minha-culpa.jpg",
        "sinopse": "A típica dinâmica de meio-irmãos que se odeiam no começo, mas que têm uma "
                   "química inegável. É o tipo de filme rápido, cheio de drama e corrida de "
                   "carro que prende do início ao fim.",
    },
    {
        "titulo": "Legalmente Loira",
        "ano": 2001,
        "mood": "Para se motivar",
        "emoji": "🎀",
        "poster": "img/legalmente-loira.png",
        "sinopse": "Elle Woods decide entrar em Harvard para recuperar o ex, mas acaba "
                   "descobrindo o próprio potencial e calando a boca de todo mundo que duvidou "
                   "dela. Um clássico de autoconfiança.",
    },
    {
        "titulo": "Nos Vemos em Vênus",
        "ano": 2023,
        "mood": "Para refletir",
        "emoji": "🌙",
        "poster": "img/nos-vemos-em-venus.jpg",
        "sinopse": "Uma road trip pela Espanha entre dois jovens que carregam traumas pesados "
                   "e estão em busca de respostas. O romance acontece de forma natural enquanto "
                   "eles tentam se curar.",
    },
    {
        "titulo": "A Cinco Passos de Você",
        "ano": 2019,
        "mood": "Para se emocionar",
        "emoji": "💔",
        "poster": "img/a-cinco-passos-de-voce.png",
        "sinopse": "Stella e Will se apaixonam no hospital, mas a condição médica deles exige "
                   "que fiquem a metros de distância. É uma história agoniante e bonita sobre "
                   "os limites do amor.",
    },
    {
        "titulo": "10 Coisas que Eu Odeio em Você",
        "ano": 1999,
        "mood": "O clássico perfeito",
        "emoji": "📼",
        "poster": "img/10-coisas-que-eu-odeio-em-voce.jpg",
        "sinopse": "Patrick é pago para sair com Kat, a garota mais difícil da escola, mas acaba "
                   "se apaixonando de verdade. Tem a melhor trilha sonora e os melhores "
                   "diálogos dos anos 90.",
    },
    {
        "titulo": "O Casamento do Meu Melhor Amigo",
        "ano": 1997,
        "mood": "Para repensar o amor",
        "emoji": "💐",
        "poster": "img/o-casamento-do-meu-melhor-amigo.jpg",
        "sinopse": "Julianne percebe que ama o melhor amigo exatamente quando ele anuncia o "
                   "casamento com outra. Ela tenta estragar tudo, mas o filme foge totalmente "
                   "do clichê esperado.",
    },
    {
        "titulo": "Meu Primeiro Amor",
        "ano": 1991,
        "mood": "Para nostalgia",
        "emoji": "🌼",
        "poster": "img/meu-primeiro-amor.jpg",
        "sinopse": "Acompanha a infância de Vada e seu melhor amigo, Thomas J., lidando com as "
                   "primeiras descobertas e perdas da vida. É sensível, simples e inesquecível.",
    },
    {
        "titulo": "De Repente 30",
        "ano": 2004,
        "mood": "Para sonhar acordada",
        "emoji": "✨",
        "poster": "img/de-repente-30.png",
        "sinopse": "Jenna faz um pedido no aniversário de 13 anos e acorda com 30, vivendo a "
                   "vida que sempre quis. Só que ela percebe que deixou para trás o melhor "
                   "amigo, Matt, e o que realmente importava. Pura vibe anos 2000.",
    },
]
