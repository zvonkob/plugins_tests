from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import RWjson


def main():

    h = get_input("inputs")
    draw_figure(h)

    # parts = split_graph(h, m=6, n=8)

    # for i, g in enumerate(parts):
    #     print(
    #         f"Graph {i}: "
    #         f"nodes={len(g)}, "
    #         f"depth={graph_depth(g)}, "
    #         f"width={graph_width(g)}"
    #     )
    #     draw_figure(g)


    candidates = generate_candidates(
        h,
        m_min=2,
        m_max=6,
        n_min=3,
        n_max=8
    )

    print("Number of candidates:", len(candidates))

    for i, g in enumerate(candidates):
        print(
            i,
            "nodes:", g.number_of_nodes(),
            "edges:", g.number_of_edges(),
            "depth:", graph_depth(g),
            "width:", graph_width(g)
        )
        draw_figure(g)




def get_input(pth):
    """prebere omrežje"""
    files = []
    for file in Path(pth).iterdir():
        if not file.is_file(): continue
        if file.suffix != ".json": continue
        if not file.stem.endswith("_RW"): continue
        files.append(file)
    i = get_input_input(files)
    # i = 4
    file = files[i-1]
    h = RWjson.RWjson_to_nx(file.parent, file.name[:-8])
    return h


def get_input_input(files):
    for i, file in enumerate(files, start=1):
        print(f"    {i}. {file.stem[:-3]}")
    while True:
        try:
            i = int(input("Izberi številko: "))
            if 1 <= i <= len(files): break
            raise ValueError
        except ValueError: continue
    print(f"    i = {i}")
    return i


# def split_graph(h, m, n):

#     if not nx.is_directed_acyclic_graph(h):
#         raise ValueError("Input graph must be a DAG")

#     if not nx.is_weakly_connected(h):
#         raise ValueError("Input graph must be connected")

#     if m < 1 or n < 1:
#         raise ValueError("m and n must both be >= 1")

#     if h.number_of_edges() == 0:
#         raise ValueError("Input graph must contain at least one edge")

#     # Start with one subgraph per original edge
#     parts = [{(u, v)} for u, v in h.edges()]

#     def make_graph(edges):
#         return h.edge_subgraph(edges).copy()

#     def valid(edges):
#         g = make_graph(edges)

#         return (
#             nx.is_weakly_connected(g)
#             and g.number_of_edges() >= 1
#             and graph_depth(g) <= m
#             and graph_width(g) <= n
#         )

#     # Repeatedly merge compatible subgraphs
#     changed = True

#     while changed:

#         changed = False

#         for i in range(len(parts)):

#             if changed:
#                 break

#             gi = make_graph(parts[i])
#             nodes_i = set(gi.nodes())

#             for j in range(i + 1, len(parts)):

#                 gj = make_graph(parts[j])
#                 nodes_j = set(gj.nodes())

#                 # Only merge subgraphs sharing a node
#                 if not nodes_i.intersection(nodes_j):
#                     continue

#                 combined = parts[i] | parts[j]

#                 if valid(combined):

#                     parts[i] = combined
#                     parts.pop(j)

#                     changed = True
#                     break

#     # Construct final DiGraphs
#     result = [make_graph(edges) for edges in parts]

#     # Final validation
#     for g in result:

#         assert nx.is_weakly_connected(g)
#         assert g.number_of_edges() >= 1
#         assert graph_depth(g) <= m
#         assert graph_width(g) <= n

#     return result


def generate_candidates(
    h,
    m_min,
    m_max,
    n_min,
    n_max
):

    if not nx.is_directed_acyclic_graph(h):
        raise ValueError("Input graph must be a DAG")

    if not nx.is_weakly_connected(h):
        raise ValueError("Input graph must be connected")

    if m_min < 1 or m_max < m_min:
        raise ValueError("Invalid depth limits")

    if n_min < 1 or n_max < n_min:
        raise ValueError("Invalid width limits")

    levels = list(nx.topological_generations(h))

    candidates = []
    seen = set()

    # Consider all consecutive level intervals
    for start in range(len(levels)):

        for end in range(start + 1, len(levels)):

            depth = end - start

            if depth < m_min:
                continue

            if depth > m_max:
                break

            nodes = {
                v
                for level in levels[start:end + 1]
                for v in level
            }

            sub = h.subgraph(nodes).copy()

            # Only connected components containing edges
            for component in nx.weakly_connected_components(sub):

                g = sub.subgraph(component).copy()

                if g.number_of_edges() == 0:
                    continue

                d = graph_depth(g)
                w = graph_width(g)

                if not (m_min <= d <= m_max):
                    continue

                if not (n_min <= w <= n_max):
                    continue

                # Unique candidate based on its edge set
                edge_key = frozenset(g.edges())

                if edge_key not in seen:
                    seen.add(edge_key)
                    candidates.append(g)

    return candidates
    

def graph_levels(h):
    """Return nodes grouped by their levels."""

    return list(nx.topological_generations(h))


def graph_depth(g):
    if len(g) == 0:
        return -1
    return nx.dag_longest_path_length(g)


def graph_width(g):
    return sum(
        1 for v in g
        if g.out_degree(v) == 0
    )


def draw_figure(G):
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    plt.figure()
    nx.draw(G,
        pos,
        with_labels=True,
        font_size=10,
        node_size=500,
        node_color="lightblue",
        arrows=True)
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    main()










