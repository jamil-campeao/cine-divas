import os
import sqlite3
import tempfile
import unittest

from app import create_app


class TestCineDivas(unittest.TestCase):
    """Testa o site usando um banco temporário (o banco real não é tocado)."""

    def setUp(self):
        # Roda antes de CADA teste: banco novo e vazio.
        arquivo, self.banco = tempfile.mkstemp(suffix=".db")
        os.close(arquivo)
        os.remove(self.banco)  # o init_app cria o arquivo do zero
        self.app = create_app({"DATABASE": self.banco, "TESTING": True})
        self.cliente = self.app.test_client()

    def tearDown(self):
        os.remove(self.banco)

    # ---------- ajudantes ----------

    def consultar(self, sql):
        conexao = sqlite3.connect(self.banco)
        resultado = conexao.execute(sql).fetchall()
        conexao.close()
        return resultado

    def cadastrar_e_logar(self):
        self.cliente.post("/cadastro", data={
            "nome": "Alice", "email": "alice@teste.com",
            "senha": "123456", "confirmar_senha": "123456",
        })
        self.cliente.post("/login", data={"email": "alice@teste.com", "senha": "123456"})

    def filme(self, **mudancas):
        dados = {"titulo": "Diário de uma Paixão", "ano": "2004", "mood": "Para chorar", "sinopse": "Noah e Allie."}
        dados.update(mudancas)
        return dados

    # ---------- banco ----------

    def test_cria_as_duas_tabelas_no_mesmo_banco(self):
        tabelas = self.consultar("SELECT name FROM sqlite_master WHERE type = 'table'")
        nomes = [t[0] for t in tabelas]
        self.assertIn("usuarios", nomes)
        self.assertIn("filmes", nomes)

    def test_filmes_iniciais_gravados_uma_vez_so(self):
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 10)
        create_app({"DATABASE": self.banco})  # "abre" o site de novo com o mesmo banco
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 10)

    # ---------- cadastro e login ----------

    def test_cadastro_grava_senha_hasheada(self):
        self.cadastrar_e_logar()
        email, senha = self.consultar("SELECT email, senha_hash FROM usuarios")[0]
        self.assertEqual(email, "alice@teste.com")
        self.assertNotEqual(senha, "123456")

    def test_cadastro_nao_aceita_email_repetido(self):
        self.cadastrar_e_logar()
        resposta = self.cliente.post("/cadastro", data={
            "nome": "Outra", "email": "alice@teste.com",
            "senha": "123456", "confirmar_senha": "123456",
        })
        self.assertIn("Já existe uma conta", resposta.get_data(as_text=True))

    def test_login_com_senha_errada(self):
        self.cadastrar_e_logar()
        self.cliente.get("/logout")
        resposta = self.cliente.post("/login", data={"email": "alice@teste.com", "senha": "errada"})
        self.assertIn("E-mail ou senha incorretos", resposta.get_data(as_text=True))

    def test_filmes_exige_login(self):
        resposta = self.cliente.get("/filmes")
        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])

    # ---------- CRUD de filmes ----------

    def test_listagem_mostra_os_filmes_do_banco(self):
        self.cadastrar_e_logar()
        html = self.cliente.get("/filmes").get_data(as_text=True)
        self.assertEqual(html.count('class="cartao-filme"'), 10)
        self.assertIn("Legalmente Loira", html)

    def test_cadastrar_filme_aparece_na_listagem(self):
        self.cadastrar_e_logar()
        self.cliente.post("/filmes/novo", data=self.filme())
        html = self.cliente.get("/filmes").get_data(as_text=True)
        self.assertIn("Diário de uma Paixão", html)
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 11)

    def test_cadastro_de_filme_valida_o_ano(self):
        self.cadastrar_e_logar()
        resposta = self.cliente.post("/filmes/novo", data=self.filme(ano="abc"))
        self.assertIn("O ano precisa ser um número", resposta.get_data(as_text=True))
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes")[0][0], 10)

    def test_editar_filme(self):
        self.cadastrar_e_logar()
        self.cliente.post("/filmes/1/editar", data=self.filme(titulo="Título Novo"))
        self.assertEqual(self.consultar("SELECT titulo FROM filmes WHERE id = 1")[0][0], "Título Novo")

    def test_excluir_filme(self):
        self.cadastrar_e_logar()
        self.cliente.post("/filmes/1/excluir")
        self.assertEqual(self.consultar("SELECT COUNT(*) FROM filmes WHERE id = 1")[0][0], 0)
        self.assertEqual(self.cliente.get("/filmes/1").status_code, 404)

    def test_busca_por_titulo(self):
        self.cadastrar_e_logar()
        html = self.cliente.get("/filmes?busca=loira").get_data(as_text=True)
        self.assertEqual(html.count('class="cartao-filme"'), 1)

    def test_paginas_abrem(self):
        for url in ["/login", "/cadastro", "/static/css/style.css"]:
            self.assertEqual(self.cliente.get(url).status_code, 200, url)

        self.cadastrar_e_logar()
        for url in ["/filmes", "/filmes/1", "/filmes/novo", "/filmes/1/editar"]:
            self.assertEqual(self.cliente.get(url).status_code, 200, url)


if __name__ == "__main__":
    unittest.main()
