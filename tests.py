# -*- coding: utf-8 -*-
"""
    Unidade de testes
"""
import unittest
import os.path
from repositorio import Repositorio
from ftp import Ftp

class Tests(unittest.TestCase):
    """ Testes """
    repositorio_teste = '/tmp/repos'

    def test_repositorio_existencia(self):
        """ Testa a classe Repositorio: existencia de arquivos """
        repositorio = Repositorio(self.repositorio_teste)

        self.assertTrue(repositorio.existe('1.pdf'))
        self.assertFalse(repositorio.existe('arquivoInexistente.pdf'))

    def test_repositorio_mover(self):
        """ Testa a classe Repositorio: mover um arquivo para o repositorio """
        repositorio = Repositorio(self.repositorio_teste)
        # cria um arquivo pra ser movido
        arquivo_a_ser_movido = '/tmp/arquivo_a_ser_movido.pdf'
        arquivo_teste = open(arquivo_a_ser_movido, 'w')
        arquivo_teste.write('teste')
        arquivo_teste.close()
        repositorio.move_arquivo_pro_repositorio(arquivo_a_ser_movido)

        self.assertFalse(repositorio.existe(arquivo_a_ser_movido))
        self.assertTrue(os.path.join(self.repositorio_teste,
                                     os.path.basename(arquivo_a_ser_movido)))

    def test_ftp(self):
        """ Testa o ftp """
        ftp = Ftp('127.0.0.1', 'anonymous', 'email@a.com')
        ftp.conecta(2121)
        ftp.muda_diretorio('')
        arquivos = ftp.lista_arquivos()
        self.assertGreater(len(arquivos), 0)
        print arquivos





