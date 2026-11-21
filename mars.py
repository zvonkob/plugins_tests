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

    if m < 0 or n < 1:
        raise ValueError("Invalid m or n")

    result = []

    def split(g):

        levels = graph_levels(g)

        if not levels:
            return

        # Split by depth, with one overlapping boundary level
        if len(levels) > m + 1:

            start = 0

            while start < len(levels):

                end = min(start + m + 1, len(levels))

                nodes = [
                    v
                    for level in levels[start:end]
                    for v in level
                ]

                split(g.subgraph(nodes).copy())

                if end == len(levels):
                    break

                start = end - 1

            return

        # Split by width
        leaves = [v for v in g if g.out_degree(v) == 0]

        if len(leaves) > n:

            for i in range(0, len(leaves), n):

                group = leaves[i:i+n]

                nodes = set(group)

                for v in group:
                    nodes.update(nx.ancestors(g, v))

                split(g.subgraph(nodes).copy())

            return

        result.append(g.copy())

    split(h)

    return result


def graph_levels(h):
    """Return nodes grouped by their levels."""

    return list(nx.topological_generations(h))


def graph_depth(h):
    levels = graph_levels(h)
    return len(levels) - 1 if levels else -1


def graph_width(h):
    return sum(1 for v in h if h.out_degree(v) == 0)


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
    