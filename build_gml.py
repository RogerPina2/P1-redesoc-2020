from csv import reader
import numpy as np
from unidecode import unidecode
from constantes import ano_final, ano_inicial
import pandas as pd

def extrai_deputados_votacoes(inicio, fim):

    deputados = {}
    votacoes = {}
    deputados_ids = []

    votacoesVotos = pd.read_csv('ArquivosLimpos/votacoesVotos-' + inicio + '-' + fim + '.csv')
    votacoesVotos = votacoesVotos.idVotacao.unique()

    for index, idVotacao in enumerate(votacoesVotos):
        votacoes[idVotacao] = index


    # Abre arquivo dos deputados para leitura.
    with open('ArquivosLimpos/deputados-' + inicio + '-' + fim + '.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()

        # Percorre todas as linhas para adicionar os deputados em seu dicionário
        for i, row in enumerate(reader(file)):

            # O id do deputado é a segunda coluna.
            id_deputado = row[0]

            # O nome do deputado é a terceira coluna.
            nome_deputado = row[1]

            # Cada chave do decionário dos deputados é o id de um deles
            # ela é relacionada ao seu nome e aos votos, que é um segundo
            # dicionário que relacionará um voto individual com um outro
            # deputado
            deputados[id_deputado] = { "nome" : nome_deputado, "votos" : [0] * len(votacoes), 'corr' : {} }
            deputados_ids.append(id_deputado)

    deputados['deputados_ids'] = deputados_ids
    return deputados, votacoes


def relaciona(inicio, fim, deputados, votacoes):

    

    # Abre arquivo para leitura.
    with open('ArquivosLimpos/votacoesVotos-' + inicio + '-' + fim + '.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()

        # Percorre todas as linhas para criar a relação de votos e deputados
        # Aqui são usados dotos os outros dicionários criados para fazer essa
        # relação que não tem uma ligação direta inicialmente
        for i, row in enumerate(reader(file)):

            # O id da votação é a segunda coluna
            id_votacao = row[0]

            # O id do tipo de voto, -1 para contra, 0 para neutro e 1 para a favor,
            # é a terceira coluna
            voto = float(row[1])

            # O id do deputado é a quarta coluna
            id_deputado = row[2]
            
            # É checado se se a relação das tabelas votações e votaçõesVotos está
            # correta
            if id_deputado in deputados:
                # Aqui é usada a relação entre proposições e seus autores 
                # para atribuir um voto para um dado deputado
                deputados[id_deputado]["votos"][votacoes[id_votacao]] = voto
                id_deputado_ = id_deputado

    zeros = [0] * len(deputados[id_deputado_]['votos'])

    for i in range(len(deputados['deputados_ids'])):
        id_deputadoA = deputados['deputados_ids'][i]
        for j in range(i+1, len(deputados['deputados_ids'])):
            id_deputadoB = deputados['deputados_ids'][j]
            votosA = deputados[id_deputadoA]['votos']
            votosB = deputados[id_deputadoB]['votos']
            if votosA != zeros and votosB != zeros:
                deputados[id_deputadoA]['corr'][id_deputadoB] = np.corrcoef(votosA,votosB)[0][1]

    del deputados['deputados_ids']
    return deputados


def cria_gml(inicio, fim, deputados):

    with open('GML/deputados-' + inicio + '-' + fim + '.gml', 'w') as file:

        # Primeira linha, que abre os colchetes da rede.
        file.write('graph [\n')

        # Segunda linha, que indica se a rede é dirigida (1) ou não (0).
        file.write('  directed 0\n')

        # Colchetes de cada nó. Você sempre precisa colocar um id (inteiro
        # ou string) e depois pode colocar os atributos adicionais que
        # quiser, contanto que sejam inteiros, floats ou strings. Se forem
        # strings, não esqueça as aspas duplas (isso vale para o id também).
        # Não esqueça também da indentação. Ela não é necessária mas ajuda
        # a deixar mais legível.
        for n in deputados.keys():
            nome = deputados[n]["nome"]
            file.write('  node [\n')
            file.write('    id {}\n'.format(n))
            file.write('    name "{}"\n'.format(nome))
            file.write('  ]\n')

        # Colchetes de cada aresta. Você sempre precisa colocar um source
        # e um target (ids de nós) e depois pode colocar os atributos
        # adicionais que quiser, contanto que sejam inteiros, floats ou
        # strings. Se forem strings, não esqueça as aspas duplas (isso
        # vale para o source e o target também). Não esqueça também da
        # indentação. Ela não é necessária mas ajuda a deixar mais legível.
        for deputadoA in deputados.keys():
            for deputadoB in deputados[deputadoA]["corr"].keys():
                peso = deputados[deputadoA]["corr"][deputadoB]
                file.write('  edge [\n')
                file.write('    source {}\n'.format(deputadoA))
                file.write('    target {}\n'.format(deputadoB))
                file.write('    weight {}\n'.format(peso))
                file.write('  ]\n')

        # Última linha, que fecha os colchetes da rede.
        file.write(']\n') 

def main():

    for legislacao in range(ano_inicial, ano_final+1, 4):
        inicio = str(legislacao)
        fim = str(legislacao+3)

        deputados, votacoes = extrai_deputados_votacoes(inicio, fim)
        relaciona(inicio, fim ,deputados, votacoes) 
        cria_gml(inicio, fim, deputados)           

    print("Build finalizado") 
    print("---------------------")
    
if __name__ == '__main__':
    main()