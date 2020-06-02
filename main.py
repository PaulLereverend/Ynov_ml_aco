import random as rand
import networkx as nx
import matplotlib.pyplot as plt
from numpy.random import choice
import time
import numpy as np
import statistics


NB_NODE_MAX = 3000
CENTRALISATION_MAX = (NB_NODE_MAX/2)
NB_LONG_MAX = 100

NB_ESSAIS = 10
NB_FOURMI = 70
node_arrive = 19
node_depart = 1
G = nx.Graph()


def init():
    for x in range(NB_NODE_MAX):
        G.add_edge(rand.randrange(0, CENTRALISATION_MAX), rand.randrange(
            0, CENTRALISATION_MAX), longueur=rand.randrange(0, NB_LONG_MAX), pheromone=1)
    # print(G.edges.data())
    nx.draw(G, with_labels=True, font_weight='bold')

# random_edge = random.choice(g.edges())


def lancer():
    taille_chemin = []
    yAxis = []
    xAxis = []
    boucle = 0
    for i in range(NB_ESSAIS):
        for j in range(NB_FOURMI):
            node = node_depart
            nodes_parcourus = [node_depart]
            while node != node_arrive:
                node = choisirNodeSuivant(node, nodes_parcourus)
                if node == -1:
                    break
                nodes_parcourus.append(node)
            if node == node_arrive:
                deposer_pheromone(nodes_parcourus)
                taille_chemin.append(len(nodes_parcourus))
        if(len(taille_chemin) > 0):
            yAxis.append(statistics.mean(taille_chemin))
            taille_chemin = []
            xAxis.append(boucle)
            boucle = boucle + 1
        evaporer()
    # print(G.edges.data())
    afficher_parcours_optimal()
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Génération')
    #ax1.set_ylabel('exp', color=color)
    ax1.plot(xAxis, yAxis, color='tab:red',
             label='Taille moyenne du parcours de la génération')
    ax1.legend()
    plt.show()
    # plt.show()


def choisirNodeSuivant(node, nodes_parcourus):
    # print(node)
    somme_longueurs = G.degree(node, weight='longueur')
    # print(somme_longueurs)
    somme_pheromones = G.degree(node, weight='pheromone')
    probs = []
    arrives = []
    if somme_longueurs == 0 or somme_pheromones == 0:
        return -1
    for node1, node2, data in G.edges(node, data=True):
        if nodes_parcourus.count(node2) <= 0:
            proba = (((1-(data['longueur']/somme_longueurs)) *
                      0.05) + (data['pheromone']/somme_pheromones * 0.95))
            probs.append(proba)
            arrives.append(node2)
    if len(arrives) == 0:
        return -1
    probs = np.array(probs)
    probs /= probs.sum()
    res = choice(arrives, size=1, p=probs)[0]
    return res


def evaporer():
    for node1, node2 in G.edges:
        G[node1][node2]['pheromone'] = round(G[node1]
                                              [node2]['pheromone']*0.05)


def deposer_pheromone(nodes_parcourus):
    # print(nodes_parcourus)
    taille_graph = G.size(weight='longueur')
    distance = 0
    iternodes = iter(nodes_parcourus)
    precedent_node = next(iternodes)
    for n in iternodes:
        distance += G[precedent_node][n]['longueur']
        precedent_node = n

    nb_a_poser = taille_graph/distance
    iternodes = iter(nodes_parcourus)
    precedent_node = next(iternodes)
    for n in iternodes:
        G[precedent_node][n]['pheromone'] += round(nb_a_poser)
        precedent_node = n


def afficher_parcours_optimal():
    print('fini')
    chemin = [node_arrive]
    node = node_arrive
    nb_essai = 0
    while node != node_depart:
        maximum = 0
        nb_essai += 1
        if nb_essai > 1000:
            print('raté')
            print(chemin)
            return None
        for node1, node2, data in G.edges(node, data=True):
            if data['pheromone'] > maximum and node2 not in chemin:
                maximum = data['pheromone']
                node = node2
        chemin.append(node)
    print('parcours optimal :')
    print(chemin)


if __name__ == "__main__":
    start_time = time.time()
    init()
    print('fin init')
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    lancer()
    print('fini')
    print("--- %s seconds ---" % (time.time() - start_time))
