# -*- coding: utf-8 -*-
"""
    Acesso ao FTP
"""
from ftplib import FTP

class Ftp(object):
    """ Representa uma conexão com servidor FTP """
    def __init__(self, servidor, usuario, senha):
        self.servidor = servidor
        self.usuario = usuario
        self.senha = senha
        self.ftp = None

    def conecta(self, porta=21):
        """ Abre a conexão """
        self.ftp = FTP()
        self.ftp.connect(self.servidor, porta)
        self.ftp.login(self.usuario, self.senha)

    def desconecta(self):
        """ Fecha a conexão """
        if self.ftp != None:
            self.ftp.quit()

    def muda_diretorio(self, novo_diretorio):
        """ Muda o diretório remoto """
        if self.ftp != None:
            self.ftp.cwd(novo_diretorio)

    def lista_arquivos(self):
        """ Retorna listagem dos arquivos """
        if self.ftp is None:
            return []
        else:
            #self.ftp.retrlines('MLSD')
            resultado = []
            self.ftp.retrlines('LIST', resultado.append)
            return resultado


