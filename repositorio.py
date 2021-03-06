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

    def __init__(self, diretorio):
        """ Inicializa o objeto """
        self.arquivos = {}
        self.diretorio = diretorio
        if os.path.isdir(self.diretorio):
            self.mascara = os.path.join(self.diretorio, '*')
        else:
            self.mascara = self.diretorio
            self.diretorio = os.path.dirname(self.diretorio)
        self.recarrega()

    def recarrega(self):
        """ Limpa o hash e recarrega do disco """
        self.arquivos.clear()
        for arquivo in glob.iglob(self.mascara):
            self.arquivos[os.path.basename(arquivo)] = os.path.getsize(arquivo)

    def existe(self, arquivo):
        """ Retorna true se o arquivo passado existe. Testa só o basename """
        arquivo = os.path.basename(arquivo)
        return self.arquivos.has_key(arquivo)

    def get_tamanho(self, arquivo):
        """ Retorna o tamanho do arquivo """
        return self.arquivos[arquivo] if self.arquivos.has_key(arquivo) else -1

    def move_arquivo_pro_repositorio(self, arquivo):
        """ Move o arquivo passado pro repositório """
        if os.path.isfile(arquivo):
            shutil.move(arquivo, self.diretorio)

    def numero_arquivos(self):
        """ Retorna a quantidade de arquivos no repositorio """
        return len(self.arquivos)

