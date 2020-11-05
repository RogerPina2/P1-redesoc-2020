#  Limpeza dos Arquivos

# Os dados disponibilizados no site da Câmara dos Deputados são dividos em diversos arquivos e 
# não estão previamente organizados para nossos objetivos. Sendo assim, é necessário realizar 
# uma limpeza nos arquivos que serão utilizados, pois iremos juntar dados de diferentes arquivos 
# que possuem algumas categorias irrelevantes. 

# Esse arquivo jupyter é responsável por documentar e realizar a limpeza dos dados baixados, 
# além de gerar as bases de dados que realmente serão utilizadas para criação de redes e análises.

# * Observação : Estamos na 56º Legislatura (2019 - 2023).


import pandas as pd
import requests
import os
from unidecode import unidecode
from constantes import ano_final, ano_inicial


def limpa_string(item):
    if isinstance(item, str):
        if 'https' in item:
            return item.split('/')[-1]
        elif item == "Não":
            return -1
        elif item == "Sim":
            return 1
        elif item == "Obstrução":
            return 0
        elif item == "Abstenção":
            return 0
        elif item == "Artigo 17":
            return 0
        else:
            return unidecode(item)
    else:
        return item

def limpa_deputados(comeco, fim):

    Legislatura2019 = 56
    diferenca = 2019 - Legislatura2019

    comeco -= diferenca
    fim -= diferenca

    file_deputados = 'ArquivosCSV/deputados.csv'
    db_deputados = pd.read_csv(file_deputados, delimiter=';')

    to_drop = [
        'cpf', 
        'urlRedeSocial', 
        'urlWebsite', 
        'dataNascimento',
        'nome',
        'nomeCivil',
        'municipioNascimento',
        'dataFalecimento',
    ]
            
    db_deputados = db_deputados.drop(columns=to_drop)
    db_deputados.columns

    start = db_deputados['idLegislaturaFinal'].between(comeco - 3, fim, inclusive=True)
    db_deputados = db_deputados.loc[start]

    end = db_deputados['idLegislaturaInicial'].between(comeco - 3, fim, inclusive=True)
    db_deputados = db_deputados.loc[end]

    db_deputados = db_deputados.applymap(limpa_string)
    db_deputados.rename(columns={ 'uri' : 'deputado_id' }, inplace=True)

    db_deputados.to_csv('ArquivosLimpos/deputados.csv', encoding='utf-8')


def limpa_votacoes(ano):
    ano = str(ano)
    file_votacoes = 'ArquivosCSV/votacoes-' + ano + '.csv'
    votacoes = pd.read_csv(file_votacoes, delimiter=';')

    to_drop = ['uri', 
            'data', 
            'dataHoraRegistro', 
            'uriOrgao',
            'siglaOrgao',
            'uriEvento',
            'descricao',
            'ultimaAberturaVotacao_dataHoraRegistro',
            'ultimaAberturaVotacao_descricao',
            'ultimaApresentacaoProposicao_dataHoraRegistro',
            'ultimaApresentacaoProposicao_descricao',
            'ultimaApresentacaoProposicao_uriProposicao'
            ]

    votacoes.drop(to_drop, inplace=True, axis=1)
    votacoes.dropna(inplace=True,axis=0)

    votacoes.to_csv('ArquivosLimpos/votacoes-' + ano + '.csv', encoding='utf-8')

def limpa_todas_votacoes(inicio, fim):
    for ano in range(inicio, fim+1):
        limpa_votacoes(ano)


def limpa_votacoesVotos(ano):
    ano = str(ano)
    votacoesVotos = pd.read_csv('ArquivosCSV/votacoesVotos-' + ano + '.csv', delimiter=';') 

    to_drop = ['uriVotacao', 
            'dataHoraVoto', 
            'deputado_uri', 
            'deputado_nome',
            'deputado_idLegislatura',
            'deputado_urlFoto'
            ]

    votacoesVotos.drop(to_drop, inplace=True, axis=1)

    votacoesVotos = votacoesVotos.applymap(limpa_string)
    votacoesVotos.rename(columns={ 'deputado_uriPartido' : 'pardido_id' }, inplace=True)

    votacoesVotos.to_csv('ArquivosLimpos/votacoesVotos-' + ano + '.csv', encoding='utf-8')

def limpa_todas_votacoesVotos(inicio, fim):
    for ano in range(inicio, fim+1):
        limpa_votacoesVotos(ano)


def limpa_proposicoesAutores(ano):
    ano = str(ano)
    proposicoesAutores = pd.read_csv('ArquivosCSV/proposicoesAutores-' + ano + '.csv', delimiter=';')

    to_drop = ['uriProposicao', 
            'uriAutor', 
            'codTipoAutor',
            'tipoAutor',
            'nomeAutor',
            'siglaPartidoAutor',
            'uriPartidoAutor',
            'siglaUFAutor',
            'ordemAssinatura',
            'proponente'
            ]

    proposicoesAutores.drop(to_drop, inplace=True, axis=1)
    proposicoesAutores.dropna(inplace=True,axis=0)

    
    proposicoesAutores.to_csv('ArquivosLimpos/proposicoesAutores-' + ano + '.csv', encoding='utf-8')

def limpa_todas_proposicoesAutores(inicio, fim):
    for ano in range(inicio, fim+1):
        limpa_proposicoesAutores(ano)


def main():

    limpa_deputados(ano_inicial, ano_final)
    limpa_todas_votacoes(ano_inicial, ano_final)
    limpa_todas_votacoesVotos(ano_inicial, ano_final)
    limpa_todas_proposicoesAutores(ano_inicial, ano_final)

if __name__ == '__main__':
    main()