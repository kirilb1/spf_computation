import json
from code.topology import Graph
from code.traffic import Traffic
from code.visualise import Visualise

import pandas as pd

print("1. Create network topology for links.csv file and print all the nodes and links")
nx_instance = Graph()
G = nx_instance.G
print(f"The nodes are: {G.nodes()}")
print(f"The links are: {G.edges()}")

print("2. Visualise network topology")
vs = Visualise(G)
vs.visualise_graph()

print("3. Map flows to link utilisations")
tf = Traffic()
links = nx_instance.links
links_util = tf.Flows_to_Loads(G, links)
main_util_df = pd.DataFrame(list(links_util.items()), columns=["links", "Baseline"])
main_util_df = main_util_df.set_index("links")

print("4. Perform failures and calculate link utilisation")
failures = json.load(open("input/failures.json"))
nodes = failures["nodes"]
for node in nodes:
    G.remove_node(node)
    links_util = tf.Flows_to_Loads(G, links)
    util_df = pd.DataFrame(list(links_util.items()), columns=["links", node])
    util_df = util_df.set_index("links")
    main_util_df = main_util_df.join(util_df, on="links")
    nx_instance = Graph()
    G = nx_instance.G

print("5. Calculate wc link utilisation")
main_util_df["wc_util"] = main_util_df.max(axis=1)
main_util_df["wc_filure"] = main_util_df.idxmax(axis=1)
print(main_util_df)
