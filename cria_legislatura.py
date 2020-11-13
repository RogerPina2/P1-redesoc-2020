import pandas as pd
import numpy as np
from unidecode import unidecode
from constantes import ano_final, ano_inicial


def main():

    proposicoes = []
    votacoes = []
    votacoesVotos = []

    for legislacao in range(ano_inicial, ano_final+1, 4):
        inicio = str(legislacao)
        fim = str(legislacao+3)
        for ano in range(legislacao, legislacao+4):
            ano = str(ano)
            file_proposicoes = 'ArquivosLimpos/proposicoesAutores-' + ano + '.csv'
            file_votacoes = 'ArquivosLimpos/votacoes-' + ano + '.csv'
            file_votacoesVotos = 'ArquivosLimpos/votacoesVotos-' + ano + '.csv'

            proposicoes.append(pd.read_csv(file_proposicoes))
            votacoes.append(pd.read_csv(file_votacoes))
            votacoesVotos.append(pd.read_csv(file_votacoesVotos))

        proposicoes = pd.concat(proposicoes)
        votacoes = pd.concat(votacoes)
        votacoesVotos = pd.concat(votacoesVotos)

        proposicoes.to_csv('ArquivosLimpos/proposicoesAutores-' + inicio + '-' + fim + '.csv', encoding='utf-8', index=False)
        votacoes.to_csv('ArquivosLimpos/votacoes-' + inicio + '-' + fim + '.csv', encoding='utf-8', index=False)
        votacoesVotos.to_csv('ArquivosLimpos/votacoesVotos-' + inicio + '-' + fim + '.csv', encoding='utf-8', index=False)

        proposicoes = []
        votacoes = []
        votacoesVotos = []

if __name__ == '__main__':
    main()