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
    file_deputados = 'ArquivosCSV/deputados.csv'
    db_deputados = pd.read_csv(file_deputados, delimiter=';')
    
    to_drop = [
        #uri', 
        #'nome', 
        #'idLegislaturaInicial', 
        #'idLegislaturaFinal',
        'nomeCivil', 
        'cpf', 
        #'siglaSexo', 
        'urlRedeSocial', 
        'urlWebsite',
        'dataNascimento', 
        'dataFalecimento', 
        'ufNascimento',
        'municipioNascimento'
    ]
    db_deputados = db_deputados.drop(columns=to_drop)

    legislatura_comeco = get_legislatura(comeco)
    legislatura_fim = get_legislatura(fim)

    comeco_ = comeco
    for legislatura in range(legislatura_comeco, legislatura_fim + 1):
        
        db_deputados = db_deputados[(db_deputados['idLegislaturaInicial'] <= legislatura) & (db_deputados['idLegislaturaFinal'] >= legislatura)]

        db_deputados = db_deputados.applymap(limpa_string)
        db_deputados.rename(columns={ 'uri' : 'deputado_id' }, inplace=True)

        db_deputados.dropna(inplace=True,axis=0)

        db_deputados.to_csv('ArquivosLimpos/deputados-' + str(comeco_) + '-' + str(comeco_+3) + '.csv', encoding='utf-8', index=False)

        comeco_ += 4


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

    votacoes.to_csv('ArquivosLimpos/votacoes-' + ano + '.csv', encoding='utf-8', index=False)

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

    votacoesVotos.dropna(inplace=True,axis=0)

    votacoesVotos.to_csv('ArquivosLimpos/votacoesVotos-' + ano + '.csv', encoding='utf-8', index=False)

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
    
    proposicoesAutores.to_csv('ArquivosLimpos/proposicoesAutores-' + ano + '.csv', encoding='utf-8', index=False)

def limpa_todas_proposicoesAutores(inicio, fim):
    for ano in range(inicio, fim+1):
        limpa_proposicoesAutores(ano)

def limpa_frentes(comeco, fim):

    legislatura_comeco = get_legislatura(comeco)
    legislatura_fim = get_legislatura(fim)

    file_frentes = 'ArquivosCSV/frentesDeputados.csv'
    frentes = pd.read_csv(file_frentes, delimiter=';')

    to_drop = [#'id', 
            'uri', 
            #'titulo', 
            #'deputado_.id', 
            'deputado_.uri',
            'deputado_.uriPartido', 
            #'deputado_.nome', 
            #'deputado_.siglaUf',
            #'deputado_.idLegislatura',
            'deputado_.urlFoto', 
            'deputado_.codTitulo',
            'deputado_.titulo',
            'dataInicio', 
            'dataFim'
    ]
    frentes = frentes.drop(columns=to_drop)

    comeco_ = comeco
    for legislatura in range(legislatura_comeco, legislatura_fim + 1):
            
        frentes = frentes[frentes['deputado_.idLegislatura'] == legislatura]

        frentes.dropna(inplace=True,axis=0)

        frentes.to_csv('ArquivosLimpos/frentes-' + str(comeco_) + '-' + str(comeco_+3) + '.csv', encoding='utf-8', index=False)
        
        comeco_ += 4


def get_legislatura(ano):
    
    if ano >= 2019: return 56
    elif ano <= 2018 and ano >= 2015: return 55
    elif ano <= 2014 and ano >= 2011: return 54
    elif ano <= 2010 and ano >= 2007: return 53
    elif ano <= 2006 and ano >= 2003: return 52
    elif ano <= 2002 and ano >= 1999: return 51
    elif ano <= 1998 and ano >= 1995: return 50
    else:
        print('Adicionar mais elifs na função get_legislatura')
        return None


def main():

    # limpa_deputados(ano_inicial, ano_final)
    # limpa_todas_votacoes(ano_inicial, ano_final)
    # limpa_todas_votacoesVotos(ano_inicial, ano_final)
    # limpa_todas_proposicoesAutores(ano_inicial, ano_final)
    limpa_frentes(ano_inicial, ano_final)

if __name__ == '__main__':
    main()