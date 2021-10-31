STATE_UNKNOWN = 0
STATE_OPENED  = 1
STATE_CLOSED  = 2

G = engine.Graph()

G.add_edges_from([
  ('a', 'b', { 'w': 30 }),
  ('a', 'c', { 'w': 40 }),
  ('b', 'c', { 'w': 50 }),
  ('c', 'd', { 'w': 15 })
])

for v in G.nodes:
  G.nodes[v]['s'] = STATE_UNKNOWN
  G.nodes[v]['h'] = float('inf')
  G.nodes[v]['p'] = None

G.color_nodes_by(prop='s', colors=[None, 'blue', 'red'])
G.label_nodes_by(prop='h')
G.label_edges_by(prop='w')

v0 = 'a'
G.nodes[v0]['s'] = STATE_OPENED
G.nodes[v0]['h'] = 0

while True:
  op = [ v for v in G.nodes if G.nodes[v]['s'] == STATE_OPENED ]

  if len(op) == 0:
    break

  op.sort(key=lambda v : G.nodes[v]['h'])

  v = op[0]

  for w in G.adj[v]:
    if G.nodes[w]['h'] > G.nodes[v]['h'] + G.edges[v, w]['w']:
      G.nodes[w]['h'] = G.nodes[v]['h'] + G.edges[v, w]['w']
      G.nodes[w]['s'] = STATE_OPENED
      G.nodes[w]['p'] = v

  G.nodes[v]['s'] = STATE_CLOSED
