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

    for ano in range(ano_inicial, ano_final+1):
        ano = str(ano)
        g = load("deputados-" + ano)
        bc = nx.betweenness_centrality(g)
        ec = nx.eigenvector_centrality(g, max_iter=10000)

        deputados = pd.read_csv('Arquivos Limpos/deputados.csv')

        deputados_bc = pd.DataFrame.from_dict(bc, orient='index', dtype=None, columns=["betweenness_centrality"])
        deputados_ec = pd.DataFrame.from_dict(ec, orient='index', dtype=None, columns=["eigenvecto_centrality"])


        deputados_inter = pd.merge(deputados,deputados_bc, left_on='deputado_id', right_on=None, right_index=True)
        deputados_final = pd.merge(deputados_inter,deputados_ec, left_on='deputado_id', right_on=None, right_index=True)


        deputados_final.to_csv('Arquivos Limpos/deputados-' + ano + '.csv', encoding='utf-8')

if __name__ == '__main__':
    main()