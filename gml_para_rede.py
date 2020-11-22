import seaborn as sns
import networkx as nx
from statistics import mean
import freeman as fm
import pandas as pd
from constantes import ano_final, ano_inicial

def load(name):
    g = fm.load('{}.gml'.format(name))

    # Remover todas as arestas com peso menor ou igual a 0.5.
    # Precisamos de dois loops, pois não é uma boa ideia
    # tirar algo de um conjunto enquanto iteramos nele.
    removed = []
    for n, m in g.edges:
        if g.edges[n, m]['weight'] <= 0.5:
            removed.append((n, m))
    for n, m in removed:
        g.remove_edge(n, m)

    # Remover todos os nós que ficaram isolados depois da
    # remoção das arestas, para melhorar a visualização.
    removed = []
    for n in g.nodes:
        if not g.degree(n):
            removed.append(n)
    for n in removed:
        g.remove_node(n)

    return g


def main():

    for legislacao in range(ano_inicial, ano_final+1, 4):
        inicio = str(legislacao)
        fim = str(legislacao+3)

        g = load("gml/deputados-" + inicio + "-" + fim)
        bc = nx.betweenness_centrality(g)
        dc = nx.degree_centrality(g)
        ec = nx.eigenvector_centrality(g, max_iter=10000)
        rm = nx.reciprocity(g)

        print("----------------------")
        print("Reciprocity {}-{}: {}".format(inicio, fim, rm))
        print("----------------------")

        deputados = pd.read_csv('ArquivosLimpos/deputados-' + inicio + '-' + fim + '.csv')

        deputados_bc = pd.DataFrame.from_dict(bc, orient='index', dtype=None, columns=["betweenness_centrality"])
        deputados_dc = pd.DataFrame.from_dict(dc, orient='index', dtype=None, columns=["degree_centrality"])
        deputados_ec = pd.DataFrame.from_dict(ec, orient='index', dtype=None, columns=["eigenvecto_centrality"])

        deputados_pre   = pd.merge(deputados,deputados_bc, left_on='deputado_id', right_on=None, right_index=True)
        deputados_inter = pd.merge(deputados_pre,deputados_dc, left_on='deputado_id', right_on=None, right_index=True)
        deputados_final = pd.merge(deputados_inter,deputados_ec, left_on='deputado_id', right_on=None, right_index=True)


        deputados_final.to_csv('ArquivosLimpos/deputados-' + inicio + '-' + fim + '.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    main()