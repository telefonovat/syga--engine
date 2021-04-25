STATE_UNKNOWN = 0
STATE_OPENED  = 1
STATE_CLOSED  = 2

G = engine.Graph()

G.add_edge('a', 'b', w=30)
G.add_edge('a', 'c', w=40)
G.add_edge('b', 'c', w=50)
G.add_edge('c', 'd', w=15)

for v in G.nodes:
  G.nodes[v]['s'] = STATE_UNKNOWN
  G.nodes[v]['h'] = float('inf')
  G.nodes[v]['p'] = None

v0 = 'a'

G.nodes[v0]['s'] = STATE_OPENED
G.nodes[v0]['h'] = 0

G.color_nodes_by(prop='s', colors=['gray', 'blue', 'red'])
G.label_nodes_by(prop='h')

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

print('-' * 60 + ' Results')
[ print('{}: {}'.format(v, G.nodes[v])) for v in G.nodes ]
