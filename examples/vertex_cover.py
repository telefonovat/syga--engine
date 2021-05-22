import random

# Components
G = engine.Graph()
G.add_edges_from(zip(random.choices(range(100), k=400), random.choices(range(100), k=400)))

cover_nodes = []
edges = list(G.edges)

# Stylization
G.color_nodes_by(cover_nodes)
G.color_edges_by(lambda u, v, G: u in cover_nodes or v in cover_nodes)

# Algorithm
while len(edges) > 0:
  u, v = random.choice(edges)
  cover_nodes += [u, v]
  [edges.remove((u, w)) for w in G.adj[u] if (u, w) in edges]
  [edges.remove((v, w)) for w in G.adj[v] if (v, w) in edges]
