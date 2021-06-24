import networkx as nx
import pandas as pd


class Traffic:
    def __init__(self):
        self.flows = self.create_flows()

    def create_flows(self):
        df = pd.read_csv("input/traffic.csv")
        my_dict = df.set_index(["node_a", "node_b"]).T.to_dict("list")
        return my_dict

    def SP_Edge(self, shortest_path, traffic):
        """for the given demand's shortest path add traffic for each edge"""
        new = {}
        for a in range(0, len(shortest_path) - 1, 1):
            new.update({(shortest_path[a], shortest_path[a + 1]): traffic})
        return new

    def max_link_util(self, dict_final, links):
        links_dict = {}
        volume = 0
        for link in links:
            reverse_link = (link[1], link[0])
            if link in dict_final and reverse_link in dict_final:
                if dict_final[link] >= dict_final[reverse_link]:
                    links_dict[link] = dict_final[link]
                else:
                    links_dict[link] = dict_final[reverse_link]
            elif link in dict_final and reverse_link not in dict_final:
                links_dict[link] = dict_final[link]
            elif link not in dict_final and reverse_link in dict_final:
                links_dict[link] = dict_final[reverse_link]
            else:
                links_dict[link] = volume
        return links_dict

    def Flows_to_Loads(self, G, links):
        dict_final = {}
        for demand_key, traffic in self.flows.items():
            shortest_path = list(
                nx.shortest_path(G, demand_key[0], demand_key[1], weight="weight")
            )
            edges = self.SP_Edge(shortest_path, traffic[0])
            for key, volume in edges.items():
                if key in dict_final:
                    dict_final[key] = int(dict_final[key]) + int(volume)
                else:
                    dict_final.update(edges)
        return self.max_link_util(dict_final, links)
