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
from ftp import Ftp, convert_bytes


def main():
    """ Dispara o programa """
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

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
    arquivos.sort(key=lambda arq: -arq.tamanho)
    baixados = 0
    ignorados = 0
    tamanho_total = 0
    pendencias = []
    for arquivo in arquivos:
        ignora = False
        tamanho_local = repositorio.get_tamanho(arquivo.nome)
        #print 'Tamanho repos %s, tamanho FTP %s' % (tamanho_local, arquivo.tamanho)
        msg = None
        if not repositorio.existe(arquivo.nome):
            msg = 'Não existe - baixando %s (%s)'
        elif tamanho_local != arquivo.tamanho:
            msg = 'Tamanho diferente - baixando %s (%s)'
        else:
            ignora = True
        if not ignora:
            pendencias.append({'nome': arquivo.nome, 'tamanho': arquivo.tamanho, 'msg': msg})
            tamanho_total += arquivo.tamanho
            baixados += 1
        else:
            #logging.debug('Arquivo já existe: %s', arquivo.nome)
            ignorados += 1
    if len(pendencias) > 0:
        logging.info('Arquivos a baixar: %s (%s)', len(pendencias), convert_bytes(tamanho_total))
        for pendencia in pendencias:
            logging.info(pendencia['msg'], pendencia['nome'], convert_bytes(pendencia['tamanho']))
            ftp.download(pendencia['nome'], pendencia['tamanho'], config.repositorio)
        logging.info('Fim do processamento, %s baixados, %s ignorados', baixados, ignorados)
    else:
        logging.info('Todos os arquivos já existem, nada a fazer')
    ftp.desconecta()


if __name__ == '__main__':
    main()
