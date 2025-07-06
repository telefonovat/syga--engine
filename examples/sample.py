# Components
G = engine.Graph()

G.add_edges_from([("a", "b", {"w": 1}), ("a", "c", {"w": 2})])

# Preparation
for v in G.nodes:
    G.nodes[v]["discovered"] = False

# Stylization
G.color_nodes_by(lambda v, G: sum(G.edges[u, v]["w"] for u in G.adj[v]))
G.label_edges_by(prop="w")

# Algorithm
# Do the magic
