import networkx as nx
from itertools import combinations
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        # punto 2
        self._N = 0
        self._grupBest = []
        self._pesoBest = -1
        self._ricavoBest = -1
        self._candidati = []

    # ==================== PUNTO 1 ====================


    def buildGraph(self):
        self._grafo.clear()
        self._idMap = {}

        # nodi: generi acquistati da clienti del paese
        nodi = DAO.getNodi()
        self._idMap = {g.id: g for g in nodi}
        self._grafo.add_nodes_from(nodi)

        # set dei clienti di ogni genere
        for idG, idC in DAO.getAlbumTrack():
            if idG in self._idMap:
                self._idMap[idG].brani.add(idC)
        for idA, idG in DAO.getGeneriAlbum():
            if idA in self._idMap:
                self._idMap[idA].generi.add(idG)

        # archi: almeno 'soglia' clienti in comune
        for g1, g2 in DAO.getEdges():
                self._grafo.add_edge(self._idMap[g1], self._idMap[g2])

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda g: g.title)

    def getComponenti(self):
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        return len(componenti), len(piuGrande)


    def getInfoComponentePiuGrande(self):
        componenti = list(nx.connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        album = sorted(piuGrande, key=lambda a:a.title)
        dettagli = []
        for a in album:
            dettagli.append((a.title,len(a.brani)))
        return dettagli

    def getSelezione(self, partenza, N):
        self._N = N
        self._solBest = []
        self._braniBest = -1
        self._comp = {}
        for indice, componente in enumerate(nx.connected_components(self._grafo)):
            for album in componente:
                self._comp[album] = indice
        self._album = list(self._grafo.nodes)
        self._ricorsione([partenza], {self._comp[partenza]}, 0)
        return self._solBest, self._braniBest

    def _ricorsione(self, parziale, compUsate, start):
        if len(parziale) == self._N:
            brani = sum(len(a.brani) for a in parziale)
            if brani > self._braniBest:
                self._braniBest = brani
                self._solBest = list(parziale)
            return
        for j in range(start, len(self._album)):
            candidato = self._album[j]
            if self._comp[candidato] in compUsate:  # componente già usata -> salto
                continue
            parziale.append(candidato)
            compUsate.add(self._comp[candidato])
            self._ricorsione(parziale, compUsate, j + 1)
            parziale.pop()
            compUsate.remove(self._comp[candidato])

    def getAlbum(self, idA):
        return self._idMap.get(idA)

    def getNumComponenti(self):
        return nx.number_connected_components(self._grafo)

