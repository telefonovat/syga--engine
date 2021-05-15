import random

# Components
G = engine.Graph()
stack = []

G = engine.Graph()
G.add_edges_from(zip(random.choices(range(100), k=400), random.choices(range(100), k=400)))
# G.add_nodes_from(range(1, 11)) # {1, 2, ..., 10}
# G.add_edges_from([
#   # Component 1
#   (1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (4, 5),
#   # Component 2
#   (6, 7),
#   # Component 3
#   (8, 9), (8, 10), (9, 10)
# ])

# Preparation
for v in G.nodes:
  G.nodes[v]['component'] = None

# Stylization
G.color_nodes_by(prop='component')

# Algorithm
c = 0

for v in G.nodes:
  if G.nodes[v]['component'] is None:
    c += 1
    stack.append(v)
    while len(stack) > 0:
      v = stack.pop()
      G.nodes[v]['component'] = c
      for u in G.adj[v]:
        if G.nodes[u]['component'] is None:
          stack.append(u)
