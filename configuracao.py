# -*- coding: utf-8 -*-
"""
    Configuração do programa

    Normalmente a partir de um JSON
"""
import json

class Configuracao(object):
    """ Representa a configuração do programa """

    def __init__(self):
        self.repositorio = None
        self.servidor = None
        self.porta = 21
        self.usuario = None
        self.senha = None
        self.diretorio = None

    def limpa(self):
        """ Limpa a configuração atual """
        self.repositorio = None
        self.servidor = None
        self.porta = 21
        self.usuario = None
        self.senha = None
        self.diretorio = None

    def carrega_de_arquivo_json(self, arquivo):
        """ Carrega a configuracao de um arquivo JSON """
        try:
            with open(arquivo, 'r') as ponteiro_arquivo:
                config = json.load(ponteiro_arquivo)
                self.repositorio = config['repositorio']
                self.servidor = config['servidor']
                self.usuario = config['usuario']
                self.senha = config['senha']
                self.diretorio = config['diretorio']
        except (OSError, IOError, ValueError):
            self.limpa()

def main():
    """ Execução de teste """
    config = Configuracao()
    config.carrega_de_arquivo_json('./config_teste.json')

if __name__ == "__main__":
    main()
