# Components
G = engine.Graph([
  ('a', 'b', { 'w': 30 }),
  ('a', 'c', { 'w': 40 }),
  ('b', 'c', { 'w': 50 }),
  ('c', 'd', { 'w': 15 }),
  ('c', 'f', { 'w': 70 }),
  ('d', 'e', { 'w': 20 }),
  ('d', 'f', { 'w': 50 }),
  ('e', 'f', { 'w': 25 }),
  ('f', 'g', { 'w': 10 })
])

# Preparation
STATE_DEFAULT = 0
STATE_OPENED  = 1
STATE_CLOSED  = 2

observing = None
shortest_path = []
start = 'a'
end = 'g'

for v in G.nodes:
  G.nodes[v]['s'] = STATE_DEFAULT
  G.nodes[v]['h'] = float('inf')
  G.nodes[v]['p'] = None

# Style
G.color_nodes_by(lambda v, G:
  'DeepSkyBlue' if v == observing else
  '#db5f57' if G.nodes[v]['s'] == STATE_OPENED else
  '#57db5f' if G.nodes[v]['s'] == STATE_CLOSED else
  None
)
G.label_nodes_by(prop='h')
G.label_edges_by(prop='w')
G.color_edges_by(shortest_path, color='#57db5f')

# Algorithm
def min_h():
  v = None
  for w in G.nodes:
    if G.nodes[w]['s'] == STATE_OPENED and (v is None or G.nodes[v]['h'] > G.nodes[w]['h']):
      v = w
  return v

G.nodes[start]['s'] = STATE_OPENED
G.nodes[start]['h'] = 0

while True:
  observing = min_h()

  if observing is None:
    break

  for w in G.adj[observing]:
    if G.nodes[w]['h'] > G.nodes[observing]['h'] + G.edges[observing, w]['w']:
      G.nodes[w]['s'] = STATE_OPENED
      G.nodes[w]['h'] = G.nodes[observing]['h'] + G.edges[observing, w]['w']
      G.nodes[w]['p'] = observing

  G.nodes[observing]['s'] = STATE_CLOSED

v = end
while G.nodes[v]['p'] is not None:
  shortest_path.append((G.nodes[v]['p'], v))
  v = G.nodes[v]['p']

print(' -> '.join([u for u, v in shortest_path[::-1]] + [shortest_path[0][1]]))
