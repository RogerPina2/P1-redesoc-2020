import pandas as pd
from constantes import ano_final, ano_inicial

def main():

    for legislacao in range(ano_inicial, ano_final+1, 4):
        inicio = str(legislacao)
        fim = str(legislacao+3)

        frentes = pd.read_csv('ArquivosLimpos/frentes-' + inicio + '-' + fim + 'csv')
        deputados = pd.read_csv('ArquivosLimpos/deputados-' + inicio + '-' + fim + 'csv')

        deputados['Frentes'] = deputados['deputado_id'].apply(lambda value: len(frentes.loc[frentes['deputado_.id'] == value]))

        deputados.to_csv('ArquivosLimpos/deputados' + inicio + '-' + fim + 'csv', encoding='utf-8', index=False)       

if __name__ == '__main__':
    main()