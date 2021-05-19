import random

SEED = 1827
random.seed(SEED)
print(f'Using seed {SEED}')

# Components
G = engine.Graph()

G.add_nodes_from(range(10))

for u in range(10):
  for v in range(u + 1, 10):
    if random.random() > 0.5:
      G.add_edge(u, v, d=random.randint(3, 15))

D = [[float('inf')] * len(G.nodes) for _ in range(len(G.nodes))]

# Preparation
for v in G.nodes:
  G.nodes[v]['discovered'] = False

# Style
G.color_nodes_by(lambda v, G: None if D[0][v] == float('inf') else D[0][v])
G.label_edges_by(lambda u, v, G: D[u][v])

# Algorithm
for v in range(len(G.nodes)):
  D[v][v] = 0

for u, v in G.edges:
  D[u][v] = G.edges[u, v]['d']
  D[v][u] = G.edges[v, u]['d']

for k in range(len(G.nodes) - 1):
  for i in range(len(G.nodes)):
    for j in range (len(G.nodes)):
      D[i][j] = min(D[i][j], D[i][k + 1] + D[k + 1][j])

print('\n'.join([' '.join([str(x).ljust(3) for x in row]) for row in D]))
