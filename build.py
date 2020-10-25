from csv import reader

from unidecode import unidecode


def main():

    deputados = {}
    proposicoes = {}
    votacoes = {}

    # Abre arquivo para leitura.
    with open('Arquivos Limpos/deputados.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()
        for i, row in enumerate(reader(file)):

            id_deputado = row[1]
            nome_deputado = row[2]

            deputados[int(id_deputado)] = { "nome" : nome_deputado, "votos" : {} }

        for linha, deputado in enumerate(deputados):
            for linha, deputado_ in enumerate(deputados):
                if deputado != deputado_:
                    deputados[deputado]["votos"][deputado_] = 0


    # Abre arquivo para leitura.
    with open('Arquivos Limpos/proposicoesAutores.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()
        for i, row in enumerate(reader(file)):

            id_proposicao = row[1]
            id_deputado = row[2]

            proposicoes[int(float(id_proposicao))] = int(float(id_deputado))

    # Abre arquivo para leitura.
    with open('Arquivos Limpos/proposicoesAutores.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()
        for i, row in enumerate(reader(file)):

            id_proposicao = row[1]
            id_deputado = row[2]

            proposicoes[int(float(id_proposicao))] = int(float(id_deputado))

    # Abre arquivo para leitura.
    with open('Arquivos Limpos/votacoes.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()
        for i, row in enumerate(reader(file)):

            id_votacao = row[1]
            id_proposicao = int(row[8])

            if id_proposicao != 0:
                votacoes[id_votacao] = id_proposicao

    # Abre arquivo para leitura.
    with open('Arquivos Limpos/votacoesVotos.csv') as file:

        # Lê uma linha do arquivo e não faz nada com ela. Nem sequer joga ela
        # para uma variável. Isso é feito apenas para ignorar o cabeçalho.
        file.readline()
        for i, row in enumerate(reader(file)):

            id_votacao = row[1]
            voto = int(row[2])
            id_deputado = int(row[3])

            if id_votacao in votacoes:
                proposicao = votacoes[id_votacao]
                if proposicao in proposicoes:
                    voto_para = proposicoes[proposicao]
                    if id_deputado != voto_para:
                        deputados[id_deputado]["votos"][voto_para] += voto



    with open('deputados.gml', 'w') as file:

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
        #
        # O módulo unidecode converte todo caractere não-ASCII para o
        # caractere ASCII mais próximo. Isso é necessário porque a
        # especificação do formato gml exige que ele seja ASCII.
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
                    peso = deputados[n]["votos"][deputado]
                    file.write('  edge [\n')
                    file.write('    source {}\n'.format(n))
                    file.write('    target {}\n'.format(deputado))
                    file.write('    weight {}\n'.format(peso))
                    file.write('  ]\n')

        # Última linha, que fecha os colchetes da rede.
        file.write(']\n')
                    


    print(deputados[204418])



if __name__ == '__main__':
    main()