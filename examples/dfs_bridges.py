# Components
G = engine.Graph(
    [
        (1, 2),
        (2, 9),
        (9, 10),
        (10, 1),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 3),
        (6, 7),
        (6, 8),
    ]
)

# Preparation
STATE_DEFAULT = 0
STATE_OPENED = 1
STATE_CLOSED = 2

for v in G.nodes:
    G.nodes[v]["state"] = STATE_DEFAULT
    G.nodes[v]["pred"] = None
    G.nodes[v]["in"] = None
    G.nodes[v]["low"] = float("inf")

t = 0
bridges = []

# Style
G.color_nodes_by(lambda v, G: G.nodes[v]["state"] == STATE_OPENED)
G.color_edges_by(
    lambda u, v, G: (G.nodes[v]["state"] == STATE_OPENED and G.nodes[v]["pred"] == u)
    or (G.nodes[u]["state"] == STATE_OPENED and G.nodes[u]["pred"] == v)
)
G.shape_edges_by(bridges, shape="dotted")
G.shape_nodes_by(
    lambda v, G: G.nodes[v]["low"] == float("inf"), shapes=["square", None]
)


# Algorithm
def dfs_bridge(v, p=None):
    nonlocal t
    t += 1

    G.nodes[v]["pred"] = p
    G.nodes[v]["state"] = STATE_OPENED
    G.nodes[v]["in"] = t

    for w in G.adj[v]:
        if G.nodes[w]["in"] is None:
            dfs_bridge(w, v)
            if G.nodes[w]["low"] >= G.nodes[w]["in"]:
                print(f'LOW({w}) = {G.nodes[w]["low"]} >= IN({w}) = {G.nodes[w]["in"]}')
                bridges.append((v, w))
            G.nodes[v]["low"] = min(G.nodes[v]["low"], G.nodes[w]["low"])

        elif w != p and G.nodes[w]["in"] < G.nodes[v]["in"]:
            G.nodes[v]["low"] = min(G.nodes[v]["low"], G.nodes[w]["in"])
            print(f'LOW({v}) = {G.nodes[v]["low"]}')

    G.nodes[v]["state"] = STATE_CLOSED


dfs_bridge(1)
