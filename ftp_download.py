# -*- coding: utf-8 -*-
"""
    Principal.

    - Pega a configuração
    - Lista o repositório
    - Pega a listagem do FTP
    - Copia tudo que não tem no repositório
"""
import sys
import logging
from configuracao import Configuracao
from repositorio import Repositorio
from ftp import Ftp

def main():
    """ Dispara o programa """
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

    if len(sys.argv) < 2:
        logging.error('Passe o arquivo de configuração JSON como argumento, por favor')
        sys.exit(1)
    config = Configuracao()
    config.carrega_de_arquivo_json(sys.argv[1])
    if not config.valido:
        logging.error('Arquivo de configuração inválido!')
        sys.exit(1)
    repositorio = Repositorio(config.repositorio)
    logging.info('Arquivos no repositório: %s', repositorio.numero_arquivos())
    ftp = Ftp(config.servidor, config.usuario, config.senha)
    ftp.conecta()
    ftp.muda_diretorio(config.diretorio)
    arquivos = ftp.lista_arquivos()
    logging.info('Arquivos no FTP: %s', len(arquivos))
    baixados = 0
    ignorados = 0
    for arquivo in arquivos:
        if not repositorio.existe(arquivo.nome):
            logging.info('Baixando %s (%s bytes)', arquivo.nome, arquivo.tamanho)
            baixados += 1
        else:
            logging.debug('Arquivo já existe: %s', arquivo.nome)
            ignorados += 1
    ftp.desconecta()
    logging.info('Fim do processamento, %s baixados, %s ignorados', baixados, ignorados)


if __name__ == '__main__':
    main()
