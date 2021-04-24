import random

# Components
G = engine.Graph()
stack = []

G.add_edges_from(zip(random.choices(range(40), k=20), random.choices(range(40), k=20)))

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
      [stack.append(u) for u in G.adj[v] if G.nodes[u]['component'] is None]
