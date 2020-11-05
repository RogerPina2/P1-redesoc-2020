from csv import reader
import numpy as np
from unidecode import unidecode
from constantes import ano_final, ano_inicial


def extrai_deputados():

    deputados = {}

    # Abre arquivo dos deputados para leitura.
    with open('ArquivosLimpos/deputados.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()

        # Percorre todas as linhas para adicionar os deputados em seu dicionário
        for i, row in enumerate(reader(file)):

            # O id do deputado é a segunda coluna.
            id_deputado = row[1]

            # O nome do deputado é a terceira coluna.
            nome_deputado = row[2]

            # Cada chave do decionário dos deputados é o id de um deles
            # ela é relacionada ao seu nome e aos votos, que é um segundo
            # dicionário que relacionará um voto individual com um outro
            # deputado
            deputados[int(id_deputado)] = { "nome" : nome_deputado, "votos" : {} }

        # Cada deputado terá a seu dicionário de votos preenchido com o id
        # de todos os outros deputados, que é relacionado com o valor 0
        for linha, deputado in enumerate(deputados):
            # Todos os deputados novamente
            for linha, deputado_ in enumerate(deputados):
                # Aqui é checado se o deputado não está sendo adicionado em
                # seu próprio dicionário
                if deputado != deputado_:
                    deputados[deputado]["votos"][deputado_] = { "numero_votos": 0, "votos_positivos" : 0, "votos_negativos" : 0 }

    return deputados


def extrai_proposicoesAutores(ano):
    ano = str(ano)
    proposicoes = {}
    # Abre arquivo para leitura.
    with open('ArquivosLimpos/proposicoesAutores-' + ano + '.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()

        # Percorre todas as linhas para criar a relação de proposicões e seus autores
        for i, row in enumerate(reader(file)):

            # O id da proposição é a segunda coluna
            id_proposicao = row[1]

            # O id do deputado é a terceira coluna
            id_deputado = row[2]

            # Esse dicionário guarda essa relação para ajudar na contrução da rede
            # Os dados são guardados com int para maoir facilidade de manuseio
            proposicoes[int(float(id_proposicao))] = int(float(id_deputado))

    return proposicoes


def extrai_votacoes(ano):
    ano = str(ano)
    votacoes = {}

    # Abre arquivo para leitura.
    with open('ArquivosLimpos/votacoes-' + ano + '.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()

        # Percorre todas as linhas para criar a relação de votações e suas proposições
        for i, row in enumerate(reader(file)):

            # O id da proposição é a segunda coluna
            id_votacao = row[1]

            # O id da proposição é a segunda coluna
            # o dado é transformado em int para maelhor manuseio
            id_proposicao = int(row[8])

            # Esse dicionário guarda essa relação para ajudar na contrução da rede
            if id_proposicao != 0:
                # Mas apenas se o id da proposição é diferente de 0, que significa
                # que seu autor não é um indivíduo, mas um orgão do governo
                votacoes[id_votacao] = id_proposicao

    return votacoes


def relaciona(ano, deputados, proposicoes, votacoes):
    ano = str(ano)

    # Abre arquivo para leitura.
    with open('ArquivosLimpos/votacoesVotos-' + ano + '.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()

        # Percorre todas as linhas para criar a relação de votos e deputados
        # Aqui são usados dotos os outros dicionários criados para fazer essa
        # relação que não tem uma ligação direta inicialmente
        for i, row in enumerate(reader(file)):

            # O id da votação é a segunda coluna
            id_votacao = row[1]

            # O id do tipo de voto, -1 para contra, 0 para neutro e 1 para a favor,
            # é a terceira coluna
            voto = int(row[2])

            # O id do deputado é a quarta coluna
            id_deputado = int(row[3])
            
            # É checado se se a relação das tabelas votações e votaçõesVotos está
            # correta
            if id_votacao in votacoes:

                proposicao = votacoes[id_votacao]

                # É checado se se a relação das tabelas votações 
                # e proposições está correta
                if proposicao in proposicoes:

                    voto_para = proposicoes[proposicao]

                    # É checado se o voto de um deputado não é direciona a ele
                    # mesmo
                    
                    if id_deputado != voto_para:
                        if id_deputado in deputados and voto_para in deputados:
                            # Aqui é usada a relação entre proposições e seus autores 
                            # para atribuir um voto para um dado deputado
                            deputados[id_deputado]["votos"][voto_para]["numero_votos"] += 1
                            if voto == 1:
                                deputados[id_deputado]["votos"][voto_para]["votos_positivos"] += 1
                            elif voto == -1:
                                deputados[id_deputado]["votos"][voto_para]["votos_negativos"] += 1

    return deputados


def cria_gml(ano, deputados):
    ano = str(ano)

    with open('deputados-' + ano + '.gml', 'w') as file:

        # Primeira linha, que abre os colchetes da rede.
        file.write('graph [\n')

        # Segunda linha, que indica se a rede é dirigida (1) ou não (0).
        file.write('  directed 1\n')

        # Colchetes de cada nó. Você sempre precisa colocar um id (inteiro
        # ou string) e depois pode colocar os atributos adicionais que
        # quiser, contanto que sejam inteiros, floats ou strings. Se forem
        # strings, não esqueça as aspas duplas (isso vale para o id também).
        # Não esqueça também da indentação. Ela não é necessária mas ajuda
        # a deixar mais legível.
        for n in deputados.keys():
            file.write('  node [\n')
            file.write('    id {}\n'.format(n))
            file.write('    name "{}"\n'.format(deputados[n]["nome"]))
            file.write('  ]\n')

        # Colchetes de cada aresta. Você sempre precisa colocar um source
        # e um target (ids de nós) e depois pode colocar os atributos
        # adicionais que quiser, contanto que sejam inteiros, floats ou
        # strings. Se forem strings, não esqueça as aspas duplas (isso
        # vale para o source e o target também). Não esqueça também da
        # indentação. Ela não é necessária mas ajuda a deixar mais legível.
        for n in deputados.keys():
            for deputado in deputados[n]["votos"]:
                if deputados[n]["votos"][deputado] != 0:
                    numero_votos = deputados[n]["votos"][deputado]["numero_votos"]
                    votos_positivos = deputados[n]["votos"][deputado]["votos_positivos"]
                    votos_negativos = deputados[n]["votos"][deputado]["votos_negativos"]
                    peso = votos_positivos - votos_negativos
                    file.write('  edge [\n')
                    file.write('    source {}\n'.format(n))
                    file.write('    target {}\n'.format(deputado))
                    file.write('    weight {}\n'.format(peso))
                    file.write('  ]\n')

        # Última linha, que fecha os colchetes da rede.
        file.write(']\n') 

def main():

    deputados = extrai_deputados()

    for ano in range(ano_inicial, ano_final+1):
        deputados_ = deputados.copy()
        proposicoes = extrai_proposicoesAutores(ano)
        votacoes = extrai_votacoes(ano)
        relaciona(ano,deputados_, proposicoes, votacoes)    
        cria_gml(ano, deputados_)           

if __name__ == '__main__':
    main()