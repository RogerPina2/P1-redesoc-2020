import requests
import os
from constantes import ano_final, ano_inicial




def main():

    print("Baixando arquivos")

    path = 'ArquivosCSV'
    files = os.listdir(path)

    nomes = [
        'frentes.csv', 
        'deputados.csv', 
        'proposicoes-{}.csv',  
        'proposicoesAutores-{}.csv', 
        'votacoes-{}.csv', 
        'votacoesVotos-{}.csv'
    ]

    urls = [
        'https://dadosabertos.camara.leg.br/arquivos/frentes/csv/{}',
        'https://dadosabertos.camara.leg.br/arquivos/deputados/csv/{}',
        'https://dadosabertos.camara.leg.br/arquivos/proposicoes/csv/{}',
        'https://dadosabertos.camara.leg.br/arquivos/proposicoesAutores/csv/{}',
        'https://dadosabertos.camara.leg.br/arquivos/votacoes/csv/{}',
        'https://dadosabertos.camara.leg.br/arquivos/votacoesVotos/csv/{}'
    ]


    for i in range(2):

        if nomes[i] not in files:
            url = urls[i].format(nomes[i])
            r = requests.get(url, allow_redirects=True)
            open(path + '/' + nomes[i], 'wb').write(r.content)
            print(" ", nomes[i])
    

    for ano in range(ano_inicial, ano_final+1):

        for i in range(2, len(nomes)):
            nome = nomes[i].format(ano)
            if  nome not in files:
                url = urls[i].format(nome)
                r = requests.get(url, allow_redirects=True)
                open(path + '/' + nome, 'wb').write(r.content)
                print(" ", nome)

    print("Requests finalizadas") 
    print("---------------------")
    
if __name__ == '__main__':
    main()