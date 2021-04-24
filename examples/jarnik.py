G = engine.Graph()
T = engine.Graph(visualize=False)

G.add_edge(1, 2, weight=10)
G.add_edge(2, 3, weight=6)
G.add_edge(4, 5, weight=5)
G.add_edge(5, 6, weight=4)
G.add_edge(7, 8, weight=1)
G.add_edge(8, 9, weight=11)

G.add_edge(1, 4, weight=7)
G.add_edge(4, 7, weight=0)
G.add_edge(2, 5, weight=8)
G.add_edge(5, 8, weight=3)
G.add_edge(3, 6, weight=2)
G.add_edge(6, 9, weight=9)

G.color_edges_by(T.edges)
G.color_nodes_by(T.nodes)

T.add_node(5)

while True:
  edges = [ (u,v,G[u][v]) for u,v in G.edges if (u in T.nodes)^(v in T.nodes) ]
  edges.sort(key=lambda tup: tup[2]['weight'])

  if len(edges) == 0:
    break
  
  T.add_edge(edges[0][0], edges[0][1])
