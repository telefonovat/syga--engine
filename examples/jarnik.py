G = engine.Graph()
T = engine.Graph(visualize=False)

G.add_edges_from(
    [
        (1, 2, {"w": 10}),
        (2, 3, {"w": 6}),
        (4, 5, {"w": 5}),
        (5, 6, {"w": 4}),
        (7, 8, {"w": 1}),
        (8, 9, {"w": 11}),
        (1, 4, {"w": 7}),
        (4, 7, {"w": 0}),
        (2, 5, {"w": 8}),
        (5, 8, {"w": 3}),
        (3, 6, {"w": 2}),
        (6, 9, {"w": 9}),
    ]
)

G.color_edges_by(T.edges)
G.color_nodes_by(T.nodes)
G.label_nodes_by(prop="w")

T.add_node(5)

while True:
    edges = [(u, v, G[u][v]) for u, v in G.edges if (u in T.nodes) ^ (v in T.nodes)]
    edges.sort(key=lambda tup: tup[2]["w"])

    if len(edges) == 0:
        break

    T.add_edge(edges[0][0], edges[0][1])
