import random

# Components
G = engine.Graph()
G.add_edges_from(zip(random.choices(range(50), k=200), random.choices(range(50), k=200)))

# Preparation
for v in G.nodes:
  G.nodes[v]['component'] = None

# Stylization
G.color_nodes_by(prop='component')

# Algorithm
stack = []
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
