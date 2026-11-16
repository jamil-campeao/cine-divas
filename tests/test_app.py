import os
import sqlite3
import tempfile
import unittest

# O banco dos testes é um arquivo temporário (precisa vir ANTES de importar o app).
BANCO_TESTE = os.path.join(tempfile.gettempdir(), "cine_divas_teste.db")
os.environ["DB_PATH"] = BANCO_TESTE

from app import create_app  # noqa: E402
from iniciar_bd import EMAIL_TESTE, SENHA_TESTE, criar_dados_iniciais, criar_tabelas  # noqa: E402


class TestCineDivas(unittest.TestCase):
    def setUp(self):
        # Antes de CADA teste: banco novo, igual a rodar o iniciar_bd.py.
        if os.path.exists(BANCO_TESTE):
            os.remove(BANCO_TESTE)
        criar_tabelas()
        criar_dados_iniciais()
        self.cliente = create_app().test_client()

    # ---------- ajudantes ----------

    def consultar(self, sql):
        conexao = sqlite3.connect(BANCO_TESTE)
        resultado = conexao.execute(sql).fetchall()
        conexao.close()
        return resultado

    def logar(self, email=EMAIL_TESTE, senha=SENHA_TESTE):
        return self.cliente.post("/login", data={"email": email, "senha": senha})

    def cadastrar(self, email):
        return self.cliente.post("/cadastro", data={
            "nome": "Alice", "email": email, "senha": "123456", "confirmar_senha": "123456",
        })

    def filme(self, **mudancas):
        dados = {"titulo": "Diário de uma Paixão", "ano": "2004", "mood": "Para chorar", "sinopse": "Noah e Allie."}
        dados.update(mudancas)
        return dados

    def html(self, url):
        return self.cliente.get(url).get_data(as_text=True)

    # ---------- iniciar_bd.py ----------

    def test_iniciar_bd_cria_tabelas_usuario_e_filmes(self):
        tabelas = [t[0] for t in self.consultar("SELECT name FROM sqlite_master WHERE type = 'table'")]
        for tabela in ["usuarios", "filmes", "avaliacoes"]:
            self.assertIn(tabela, tabelas)
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM usuarios")[0][0], 1)
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 10)

    def test_iniciar_bd_rodar_de_novo_nao_duplica(self):
        criar_tabelas()
        criar_dados_iniciais()
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM usuarios")[0][0], 1)
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 10)

    # ---------- autenticação ----------

    def test_cadastro_grava_senha_hasheada(self):
        self.cadastrar("alice@teste.com")
        senha = self.consultar("SELECT senha_hash FROM usuarios WHERE email = 'alice@teste.com'")[0][0]
        self.assertNotEqual(senha, "123456")

    def test_cadastro_nao_aceita_email_repetido(self):
        resposta = self.cadastrar(EMAIL_TESTE)
        self.assertIn("Já existe uma conta", resposta.get_data(as_text=True))

    def test_login_errado_mostra_flash(self):
        resposta = self.logar(senha="errada")
        self.assertIn("E-mail ou senha incorretos", resposta.get_data(as_text=True))

    def test_login_grava_sessao_e_cookie(self):
        resposta = self.logar()
        self.assertIn("ultimo_email=" + EMAIL_TESTE, resposta.headers["Set-Cookie"])
        with self.cliente.session_transaction() as sessao:
            self.assertEqual(sessao["user_id"], 1)
            self.assertEqual(sessao["username"], "Diva Teste")

    def test_cookie_preenche_email_no_login(self):
        self.logar()
        self.cliente.get("/logout")
        self.assertIn(f'value="{EMAIL_TESTE}"', self.html("/login"))

    def test_middleware_bloqueia_anonimo(self):
        resposta = self.cliente.get("/filmes")
        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])

    def test_middleware_valida_usuario_no_banco(self):
        with self.cliente.session_transaction() as sessao:
            sessao["user_id"] = 999  # usuária que não existe
        self.assertEqual(self.cliente.get("/filmes").status_code, 302)

    # ---------- filmes ----------

    def test_listagem_mostra_os_filmes_da_usuaria(self):
        self.logar()
        self.assertEqual(self.html("/filmes").count('class="cartao-filme"'), 10)

    def test_cadastrar_filme_aparece_na_listagem(self):
        self.logar()
        self.cliente.post("/filmes/novo", data=self.filme())
        self.assertIn("Diário de uma Paixão", self.html("/filmes"))

    def test_validacao_do_filme(self):
        self.logar()
        self.assertIn("entre 1900 e 2100", self.cliente.post("/filmes/novo", data=self.filme(ano="abc")).get_data(as_text=True))
        self.assertIn("até 100", self.cliente.post("/filmes/novo", data=self.filme(titulo="x" * 101)).get_data(as_text=True))
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 10)

    def test_editar_filme(self):
        self.logar()
        self.cliente.post("/filmes/1/editar", data=self.filme(titulo="Título Novo"))
        self.assertEqual(self.consultar("SELECT titulo FROM filmes WHERE id = 1")[0][0], "Título Novo")

    def test_excluir_filme(self):
        self.logar()
        self.cliente.post("/filmes/1/excluir")
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes WHERE id = 1")[0][0], 0)

    def test_busca_por_titulo(self):
        self.logar()
        self.assertEqual(self.html("/filmes?busca=loira").count('class="cartao-filme"'), 1)

    def test_outra_usuaria_nao_ve_nem_apaga_filmes(self):
        self.cadastrar("alice@teste.com")
        self.logar("alice@teste.com", "123456")
        self.assertEqual(self.html("/filmes").count('class="cartao-filme"'), 0)
        self.assertEqual(self.cliente.get("/filmes/1").status_code, 404)
        self.assertEqual(self.cliente.post("/filmes/1/excluir").status_code, 404)
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 10)

    # ---------- avaliações ----------

    def test_avaliar_listar_e_excluir(self):
        self.logar()
        self.cliente.post("/filmes/1/avaliacoes", data={"nota": "5", "comentario": "Amei!"})
        self.assertIn("Amei!", self.html("/filmes/1"))
        self.assertIn("Amei!", self.html("/avaliacoes"))

        self.cliente.post("/avaliacoes/1/excluir")
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM avaliacoes")[0][0], 0)

    def test_validacao_da_nota(self):
        self.logar()
        resposta = self.cliente.post("/filmes/1/avaliacoes", data={"nota": "9"}, follow_redirects=True)
        self.assertIn("nota de 1 a 5", resposta.get_data(as_text=True))
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM avaliacoes")[0][0], 0)

    def test_excluir_filme_apaga_avaliacoes_em_cascata(self):
        self.logar()
        self.cliente.post("/filmes/1/avaliacoes", data={"nota": "4"})
        self.cliente.post("/filmes/1/excluir")
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM avaliacoes")[0][0], 0)

    # ---------- erros e páginas ----------

    def test_pagina_404_personalizada(self):
        resposta = self.cliente.get("/nao-existe")
        self.assertEqual(resposta.status_code, 404)
        self.assertIn("ops, 404", resposta.get_data(as_text=True))

    def test_paginas_abrem(self):
        for url in ["/login", "/cadastro", "/static/css/style.css"]:
            with self.cliente.get(url) as resposta:
                self.assertEqual(resposta.status_code, 200, url)
        self.logar()
        for url in ["/filmes", "/filmes/1", "/filmes/novo", "/filmes/1/editar", "/avaliacoes"]:
            self.assertEqual(self.cliente.get(url).status_code, 200, url)


if __name__ == "__main__":
    unittest.main()
