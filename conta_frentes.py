import pandas as pd


def main():

    frentes = pd.read_csv('ArquivosLimpos/frentes.csv')
    deputados = pd.read_csv('ArquivosLimpos/deputados-2015-2018.csv')

    deputados['Frentes'] = deputados['deputado_id'].apply(lambda value: len(frentes.loc[frentes['deputado_.id'] == value]))

    deputados.to_csv('ArquivosLimpos/deputados-2015-2018.csv', encoding='utf-8', index=False)       

if __name__ == '__main__':
    main()