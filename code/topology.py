from code.traffic import Traffic
from code.visualise import Visualise

import networkx as nx
import pandas as pd


class Graph:
    def __init__(self):
        self.G = self.create_graph()
        self.links = self.G.to_undirected().edges()

    def create_graph(self):
        df = pd.read_csv("input/links.csv")
        G = nx.from_pandas_edgelist(
            df, "node_a", "node_b", ["metric"], create_using=nx.DiGraph()
        )
        return G
