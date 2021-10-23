import random

NODES = random.randint(8, 15)

# Components
G = engine.Graph()

G.add_nodes_from(range(NODES))

for u in range(NODES):
  for v in range(u + 1, NODES):
    if random.random() < 0.4:
      G.add_edge(u, v)

# Preparation
STATE_DEFAULT = 0
STATE_OPENED = 1
STATE_CLOSED = 2

for v in G.nodes:
  G.nodes[v]['state'] = STATE_DEFAULT

# Style
G.color_nodes_by(lambda v, G: G.nodes[v]['state'] == STATE_OPENED)
# G.color_edges_by(queue)

# Algorithm
def dfs_step(u):
  G.nodes[u]['state'] = STATE_OPENED

  for v in G.adj[u]:
    if G.nodes[v]['state'] == STATE_DEFAULT:
      dfs_step(v)

  G.nodes[u]['state'] = STATE_CLOSED

for u in G.nodes:
  if G.nodes[u]['state'] == STATE_DEFAULT:
    print(f'Starting in {u}')
    dfs_step(u)
