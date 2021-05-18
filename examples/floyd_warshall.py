import random

# Components
G = engine.Graph()

G.add_nodes_from(range(10))

for u in range(10):
  for v in range(u, 10):
    if u != v and random.random() > 0.5:
      G.add_edge(u, v, d=random.randint(5, 10))

D = [[float('inf')] * len(G.nodes) for _ in range(len(G.nodes))]

# Preparation
for v in G.nodes:
  G.nodes[v]['discovered'] = False

# Style
G.color_nodes_by(lambda v, G: None if D[0][v] == float('inf') else D[0][v])
G.label_edges_by(lambda u, v, G: D[u][v])

# Algorithm
for u, v in G.edges:
  D[u][v] = G.edges[u, v]['d']
  D[v][u] = G.edges[v, u]['d']

print('The initial distance matrix is')
print('\n'.join([str(row) for row in D]))

for k in range(len(G.nodes) - 1):
  for i in range(len(G.nodes)):
    for j in range (len(G.nodes)):
      D[i][j] = min(D[i][j], D[i][k + 1] + D[k + 1][j])

print("The distance matrix is")
print('\n'.join([str(row) for row in D]))
