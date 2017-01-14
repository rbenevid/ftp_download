# -*- coding: utf-8 -*-
"""
    Operações sobre o repositório:
    - verifica existência de PDF
    - move um arquivo pro repositório
"""
import glob
import os.path
import shutil

class Repositorio(object):
    """ Representa o repositório local de pdfs """
    arquivos = {}

    def __init__(self, diretorio):
        """ Inicializa o objeto """
        self.diretorio = diretorio
        if os.path.isdir(self.diretorio):
            self.mascara = os.path.join(self.diretorio, '*.pdf')
        else:
            self.mascara = self.diretorio
            self.diretorio = os.path.dirname(self.diretorio)
        self.recarrega()

    def recarrega(self):
        """ Limpa o hash e recarrega do disco """
        self.arquivos.clear()
        for arquivo in glob.iglob(self.mascara):
            self.arquivos[os.path.basename(arquivo)] = 1

    def existe(self, arquivo):
        """ Retorna true se o arquivo passado existe. Testa só o basename """
        arquivo = os.path.basename(arquivo)
        return self.arquivos.has_key(arquivo)

    def move_arquivo_pro_repositorio(self, arquivo):
        """ Move o arquivo passado pro repositório """
        if os.path.isfile(arquivo):
            shutil.move(arquivo, self.diretorio)

