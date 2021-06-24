import re

import matplotlib.pyplot as plt
import networkx as nx


class Visualise:
    def __init__(self, G):
        self.G = G

    def visualise_graph(self):
        pos = nx.spring_layout(self.G)
        nx.draw(
            self.G, pos, with_labels=True, arrows=False, node_size=1000
        )  # generic graph layout
        nodelist = [
            x for x in self.G.nodes() if re.search("pe[0-9]", x)
        ]  # create a list containing PE nodes only
        nx.draw_networkx_nodes(
            self.G, pos, nodelist=nodelist, node_color="r", node_size=1000
        )  # change PE node colour to red
        edge_labels = dict(
            [
                (
                    (
                        u,
                        v,
                    ),
                    d["metric"],
                )  # create a dictionary with edges and weights
                for u, v, d in self.G.edges(data=True)
            ]
        )
        nx.draw_networkx_edge_labels(
            self.G, pos, edge_labels=edge_labels
        )  # draw edge labels
        plt.show()
