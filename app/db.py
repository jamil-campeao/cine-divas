import sqlite3

from flask import current_app, g


# ==================================================
# ESTRUTURA DAS TABELAS (as duas ficam no mesmo banco)
# ==================================================

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    criado_em  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS filmes (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo  TEXT NOT NULL,
    ano     INTEGER NOT NULL,
    mood    TEXT NOT NULL,
    sinopse TEXT NOT NULL,
    emoji   TEXT NOT NULL DEFAULT '🎬',
    poster  TEXT NOT NULL DEFAULT ''
);
"""


# ==================================================
# FILMES INICIAIS (gravados só quando a tabela está vazia)
# Ordem: titulo, ano, mood, sinopse, emoji, poster
# ==================================================

FILMES_INICIAIS = [
    (
        "Como Perder um Homem em 10 Dias", 2003, "Para rir",
        "Ela quer que ele termine com ela, e ele apostou que consegue fazê-la se apaixonar. O resultado são duas pessoas se testando ao limite enquanto tudo dá errado. É muito bom.",
        "💋", "img/como-perder-um-homem-em-10-dias.jpg"
    ),
    (
        "A Culpa é das Estrelas", 2014, "Para chorar",
        "A história de Hazel e Augustus em um grupo de apoio é bonita e dolorosa na mesma medida. Um daqueles romances que marcam e que com certeza vão te fazer chorar no final.",
        "⭐", "img/a-culpa-e-das-estrelas.png"
    ),
    (
        "Minha Culpa", 2023, "Para viciar",
        "A típica dinâmica de meio-irmãos que se odeiam no começo, mas que têm uma química inegável. É o tipo de filme rápido, cheio de drama e corrida de carro que prende do início ao fim.",
        "🏎️", "img/minha-culpa.jpg"
    ),
    (
        "Legalmente Loira", 2001, "Para se motivar",
        "Elle Woods decide entrar em Harvard para recuperar o ex, mas acaba descobrindo o próprio potencial e calando a boca de todo mundo que duvidou dela. Um clássico de autoconfiança.",
        "🎀", "img/legalmente-loira.png"
    ),
    (
        "Nos Vemos em Vênus", 2023, "Para refletir",
        "Uma road trip pela Espanha entre dois jovens que carregam traumas pesados e estão em busca de respostas. O romance acontece de forma natural enquanto eles tentam se curar.",
        "🌙", "img/nos-vemos-em-venus.jpg"
    ),
    (
        "A Cinco Passos de Você", 2019, "Para se emocionar",
        "Stella e Will se apaixonam no hospital, mas a condição médica deles exige que fiquem a metros de distância. É uma história agoniante e bonita sobre os limites do amor.",
        "💔", "img/a-cinco-passos-de-voce.png"
    ),
    (
        "10 Coisas que Eu Odeio em Você", 1999, "O clássico perfeito",
        "Patrick é pago para sair com Kat, a garota mais difícil da escola, mas acaba se apaixonando de verdade. Tem a melhor trilha sonora e os melhores diálogos dos anos 90.",
        "📼", "img/10-coisas-que-eu-odeio-em-voce.jpg"
    ),
    (
        "O Casamento do Meu Melhor Amigo", 1997, "Para repensar o amor",
        "Julianne percebe que ama o melhor amigo exatamente quando ele anuncia o casamento com outra. Ela tenta estragar tudo, mas o filme foge totalmente do clichê esperado.",
        "💐", "img/o-casamento-do-meu-melhor-amigo.jpg"
    ),
    (
        "Meu Primeiro Amor", 1991, "Para nostalgia",
        "Acompanha a infância de Vada e seu melhor amigo, Thomas J., lidando com as primeiras descobertas e perdas da vida. É sensível, simples e inesquecível.",
        "🌼", "img/meu-primeiro-amor.jpg"
    ),
    (
        "De Repente 30", 2004, "Para sonhar acordada",
        "Jenna faz um pedido no aniversário de 13 anos e acorda com 30, vivendo a vida que sempre quis. Só que ela percebe que deixou para trás o melhor amigo, Matt, e o que realmente importava. Pura vibe anos 2000.",
        "✨", "img/de-repente-30.png"
    ),
]


# ==================================================
# CONEXÃO (a única do projeto)
# ==================================================

def get_db():
    """Abre a conexão uma vez por requisição e reaproveita."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row  # permite linha["titulo"]
    return g.db


def close_db(error=None):
    """Fecha a conexão no fim da requisição (chamada pelo Flask)."""
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


# ==================================================
# INICIALIZAÇÃO (roda uma única vez, quando o site abre)
# ==================================================

def init_app(app):
    """Cria as tabelas, grava os filmes iniciais e registra o close_db."""
    app.teardown_appcontext(close_db)

    with app.app_context():
        conexao = get_db()
        conexao.executescript(SCHEMA)

        total = conexao.execute("SELECT COUNT(*) FROM filmes").fetchone()[0]
        if total == 0:
            conexao.executemany(
                "INSERT INTO filmes (titulo, ano, mood, sinopse, emoji, poster) VALUES (?, ?, ?, ?, ?, ?)",
                FILMES_INICIAIS,
            )

        conexao.commit()
