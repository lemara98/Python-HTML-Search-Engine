import matplotlib.pyplot as plot
import networkx as nx
import numpy as np
from random import random
import os

class GraphResult:
    def __init__(self):
        self.graf = nx.DiGraph ()
        self.node_sizes = []
        self.node_colors = {}
        self.colors = []
        self.edge_colors = []
        self.node_rang = {}

    def prikazi_graficki_rezultat(self):

        for i in self.graf.nodes:
            self.node_colors[i] = (random (), random (), random ()) # Boja u mapi

        for i in self.graf.nodes:
            self.node_sizes.append (50000000 / len (self.graf.nodes) * self.node_rang[i])         # Velicina cvora

        for i, j in self.graf.edges:
            self.edge_colors.append (self.node_colors[i])   # Boja veza u listi

        for i, j in self.node_colors.items():               # Boja cvorova u listi
            self.colors.append(j)

        nx.draw (self.graf, with_labels=True, node_color=self.colors, node_size=self.node_sizes,
                 edge_color=self.edge_colors)
        # plot.savefig("graph.png")
        print("Broj cvorova = ", len (self.graf.nodes))
        print("Broj veza = ", len (self.graf.edges))
        plot.show ()

    def dodajCvorUGraf(self, filename, listaPokazivacaCvora, rangCvora):
        self.graf.add_node(os.path.basename(filename))
        s = []
        self.node_rang[filename] = rangCvora
        for i in listaPokazivacaCvora:
            s.append((filename, os.path.basename(i)))
            self.graf.add_edges_from(s)