# -*- coding: utf-8 -*-
"""
    Acesso ao FTP
"""
import logging
import os.path
import time
from ftplib import FTP

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    if isinstance(num, str):
        num = int(num)
    for unidade in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, unidade)
        num /= 1024.0

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

    def download(self, item, tamanho, destino):
        """ Faz o download do item """
        down = DownloadFtp(item, tamanho, destino)
        self.ftp.retrbinary('RETR %s' % item, down.grava_dados, 65536)
        down.close()


class DownloadFtp(object):
    """ Auxilia o download FTP """
    def __init__(self, arquivo, tamanho, destino):
        self.arquivo = arquivo
        self.destino = destino
        self.tamanho = int(tamanho)
        if os.path.isdir(self.destino):
            self.destino = os.path.join(self.destino, self.arquivo)
        self.andamento = 0
        self.ponteiro = open(self.destino, 'w')
        self.start = time.time()

    def close(self):
        """ Fecha o ponteiro do arquivo """
        fim = time.time()
        elapsed = fim - self.start
        if elapsed == 0:
            velocidade = 'n/a'
        else:
            velocidade = self.andamento / elapsed
        print ''
        logging.info('Download concluído. Tempo %ss. Velocidade %s bytes/sec',
                     round(elapsed, 1), convert_bytes(velocidade))
        self.ponteiro.close()

    def grava_dados(self, dados):
        """ Andamento do download """
        tamanho = len(dados)
        if self.tamanho is not None and self.tamanho > 0:
            self.andamento += tamanho
            perc = self.andamento * 100.0 / self.tamanho
            print '\rAndamento: %.1f%%' % (perc),
        self.ponteiro.write(dados)


class EntradaFtp(object):
    """ Representa um arquivo no ftp """
    tipo = None
    data = None
    nome = None
    tamanho = None

    def __init__(self, linha_mlsd):
        logging.debug(linha_mlsd)
        for item in linha_mlsd.split(';'):
            atribuicao = item.partition('=')
            if atribuicao[1] == '=':
                campo = atribuicao[0]
                if campo == 'type':
                    self.tipo = atribuicao[2]
                elif campo == 'modify':
                    self.data = atribuicao[2]
                elif campo == 'size':
                    self.tamanho = int(atribuicao[2])
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
