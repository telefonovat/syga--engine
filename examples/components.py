import random

# Components
G = engine.Graph()
# G.add_edges_from(zip(random.choices(range(50), k=200), random.choices(range(50), k=200)))

G.add_edges_from(
    [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (3, 4),
        (4, 5),  # Component 1
        (6, 7),  # Component 2
        (8, 9),
        (8, 10),
        (9, 10),  # Component 3
        (11, 12),
        (11, 13),
        (12, 13),
        (13, 14),
        (14, 11),  # Component 4
    ]
)

# Preparation
for v in G.nodes:
    G.nodes[v]["component"] = None


# Style
def color_edges(u, v, G):
    if G.nodes[u]["component"] is not None:
        return G.nodes[u]["component"]

    if G.nodes[v]["component"] is not None:
        return G.nodes[v]["component"]

    return None


G.color_nodes_by(prop="component")
G.color_edges_by(color_edges)

# Algorithm
stack = []
c = 0

for v in G.nodes:
    if G.nodes[v]["component"] is None:
        c += 1
        print(f"Entering component {c}")
        stack.append(v)
        while len(stack) > 0:
            v = stack.pop()
            G.nodes[v]["component"] = c
            for u in G.adj[v]:
                if G.nodes[u]["component"] is None:
                    stack.append(u)

        print(f"Leaving component {c}")
