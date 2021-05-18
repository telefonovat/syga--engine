from collections import deque

# Components
G = engine.Graph()

G.add_nodes_from(range(10))

G.add_edges_from([
  (0, 1),
  (0, 3),
  (0, 9),
  (1, 2),
  (1, 3),
  (3, 4),
  (3, 6),
  (6, 7),
  (9, 6)
])

# Preparation
for v in G.nodes:
  G.nodes[v]['layer'] = -1

# Stylization
G.color_nodes_by(lambda v, G: (G.nodes[v]['layer'] + 1) or None)

# Algorithm
v0 = 1
queue = deque()

queue.append(v0)
G.nodes[v0]['layer'] = 0

while queue:
  v = queue.popleft()

  for u in G.adj[v]:
    if G.nodes[u]['layer'] == -1:
      G.nodes[u]['layer'] = G.nodes[v]['layer'] + 1
      queue.append(u)
