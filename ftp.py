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
            resultado = []
            retorno = []
            self.ftp.retrlines('MLSD', resultado.append)
            for cada_linha in resultado:
                entrada = EntradaFtp(cada_linha)
                if entrada.is_file():
                    retorno.append(entrada)
            return retorno


class EntradaFtp(object):
    """ Representa um arquivo no ftp """
    tipo = None
    data = None
    nome = None

    def __init__(self, linha_mlsd):
        for item in linha_mlsd.split(';'):
            atribuicao = item.partition('=')
            if atribuicao[1] == '=':
                campo = atribuicao[0]
                if campo == 'type':
                    self.tipo = atribuicao[2]
                elif campo == 'modify':
                    self.data = atribuicao[2]
            else:
                self.nome = item.strip()

    def is_file(self):
        """ Retorna true se for arquivo """
        return self.tipo == 'file' or self.tipo is None

    def to_string(self):
        """ Retorna uma descrição amigável do item """
        return '%s - %s - %s' % (self.tipo, self.data, self.nome)

if __name__ == "__main__":
    """ Como teste, lista o conteúdo de um ftp da internet """
    ftp = Ftp('ftp.funet.fi', 'anonymous', 'senha_qualquer')
    ftp.conecta()
    ftp.muda_diretorio('/pub/msx')
    for cada in ftp.lista_arquivos():
        print cada.to_string()
    ftp.desconecta()
