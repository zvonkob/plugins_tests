from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import RWjson


def main():

    h = get_input("inputs")
    draw_figure(h)

    parts = split_graph(h, m=2, n=3)

    for i, g in enumerate(parts):
        print(
            f"Graph {i}: "
            f"nodes={len(g)}, "
            f"depth={graph_depth(g)}, "
            f"width={graph_width(g)}"
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
    # i = get_input_input(files)
    i = 4
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


def split_graph(h, m, n):

    if not nx.is_directed_acyclic_graph(h):
        raise ValueError("Graph must be a DAG")

    if m < 1 or n < 1:
        raise ValueError("m must be >= 1 and n must be >= 1")

    if not nx.is_weakly_connected(h):
        raise ValueError("Input graph must be connected")

    roots = [v for v in h if h.in_degree(v) == 0]

    if len(roots) != 1:
        raise ValueError("Graph must have exactly one root")

    result = []

    # Nodes grouped by their levels
    levels = list(nx.topological_generations(h))

    # Recursive partitioning
    def split(g):

        if g.number_of_edges() == 0:
            return

        leaves = [v for v in g if g.out_degree(v) == 0]

        # Check whether the graph is valid
        if graph_depth(g) <= m and len(leaves) <= n:
            result.append(g.copy())
            return

        # Split by depth
        if graph_depth(g) > m:

            gens = list(nx.topological_generations(g))

            # Overlapping sections
            start = 0

            while start < len(gens) - 1:

                end = min(start + m + 1, len(gens))

                nodes = {
                    v for level in gens[start:end]
                    for v in level
                }

                # Add one predecessor level to connect the section
                if start > 0:
                    nodes.update(gens[start - 1])

                sub = g.subgraph(nodes).copy()

                split(sub)

                if end == len(gens):
                    break

                start = end - 1

            return

        # Split by width
        leaves = list(leaves)

        for i in range(0, len(leaves), n):

            group = leaves[i:i+n]

            nodes = set(group)

            for v in group:
                nodes.update(nx.ancestors(g, v))

            sub = g.subgraph(nodes).copy()

            split(sub)

    split(h)

    # # Final validation
    # for g in result:
    #     assert g.number_of_edges() >= 1
    #     assert nx.is_weakly_connected(g)
    #     assert graph_depth(g) <= m
    #     assert graph_width(g) <= n

    return result


def graph_levels(h):
    """Return nodes grouped by their levels."""

    return list(nx.topological_generations(h))


def graph_depth(g):
    if len(g) == 0:
        return -1
    return nx.dag_longest_path_length(g)


def graph_width(g):
    return sum(1 for v in g if g.out_degree(v) == 0)


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
    
