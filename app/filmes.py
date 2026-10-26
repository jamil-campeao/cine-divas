# Somente leitura, para cadastrar um novo filme, colocar aqui
FILMES = [
    {
        "slug": "como-perder-um-homem-em-10-dias",
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
        "slug": "a-culpa-e-das-estrelas",
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
        "slug": "minha-culpa",
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
        "slug": "legalmente-loira",
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
        "slug": "nos-vemos-em-venus",
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
        "slug": "a-cinco-passos-de-voce",
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
        "slug": "10-coisas-que-eu-odeio-em-voce",
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
        "slug": "o-casamento-do-meu-melhor-amigo",
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
        "slug": "meu-primeiro-amor",
        "titulo": "Meu Primeiro Amor",
        "ano": 1991,
        "mood": "Para nostalgia",
        "emoji": "🌼",
        "poster": "img/meu-primeiro-amor.jpg",
        "sinopse": "Acompanha a infância de Vada e seu melhor amigo, Thomas J., lidando com as "
                   "primeiras descobertas e perdas da vida. É sensível, simples e inesquecível.",
    },
    {
        "slug": "de-repente-30",
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


def buscar_filme(slug):
    return next((f for f in FILMES if f["slug"] == slug), None)
