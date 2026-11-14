"""
    SPREHOD ŠIRINO
        IN 
    SPREHOD V GLOBINO
        PO
    NETWORKX.DIGRAPH()
"""


import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import re

import RWjson


def main():

    file, sw_width = get_input("inputs")

    h = RWjson.RWjson_to_nx(
            file.parent, 
            file.name[:-8]
    )

    print("nodes", h.number_of_nodes())
    print("edges", h.number_of_edges())

    for id in h.nodes():
        if h.in_degree(id) == 0:
            h.cTP = id
            break

    wwidth = walk_width(h, sw_width)

    print(len(wwidth), type(wwidth))
    print(wwidth)
  
    # for w in wwidth:
    #     print(w)

    for i, w in enumerate(wwidth):
        q = h.nodes[w]
        q['w'] = i

    m, n = m_times_n(h, h.cTP)

    print()
    for vid, q in h.nodes(data=True):
        w = q["w"]
        m = q["m"]
        n = q["n"]
        print(f"{vid} w={w}, m={m}, n={n}")

    for vid1, vid2, qq in h.edges(data=True):
        q = h.nodes[vid2]
        qq["w"] = q["w"]


    draw_figure(h)


def get_input(pth):

    files = []
    for file in Path(pth).iterdir():
        if not file.is_file():
            continue
        if file.suffix != ".json":
            continue
        if not file.stem.endswith("_RW"):
            continue
        files.append(file)

    # for i, file in enumerate(files, start=1):
        # print(f"    {i}. {file}")

    for i, file in enumerate(files, start=1):
        print(f"    {i}. {file.stem[:-3]}")

    # while True:
        # try:
        #     i = int(input("Izberi številko: "))
        #     if 1 <= i <= len(files):
        #         break
        #     raise ValueError
        # except ValueError:
        #     continue

    i = 1
    print(f"    i = {i}")

    print("    1. width first")
    print("    2. depth first")

    # while True:
    #     try:
    #         j = int(input("Izberi številko: "))
    #         if j == 1:
    #             sw_width = True
    #             break
    #         if j == 2:
    #             sw_width = False
    #             break
    #         raise ValueError
    #     except ValueError:
    #         continue

    j = 1
    sw_width = True
    print(f"    j = {j}, sw_width = {sw_width}")

    return files[i-1], sw_width


def draw_figure(G):

    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    plt.figure()
    nx.draw(
        G,
        pos,
        with_labels=True,
        font_size=10,
        node_size=500,
        node_color="lightblue",
        arrows=True
    )
    plt.axis("equal")
    plt.show()


def walk_width(h, sw_width=True):

    rez = []
    todo = [ h.cTP ]
    while todo:
        if sw_width:
            c = todo.pop(0)
        else:
            c = todo.pop()
        rez.append(c)
        for d in h.successors(c):
            todo.append(d)

    return rez


def m_times_n(h, c):
    print(f"c = {c}")
    if h.out_degree(c) == 0:
        m, n = 0, 1
    else:
        m, n = 0, 0
        for d in h.successors(c):
            print(f"    d = {d}")
            md, nd = m_times_n(h, d)
            if md > m:
                m = md
            n += nd
        m += 1
    h.nodes[c]["m"], h.nodes[c]["n"] = m, n
    return m, n


if __name__ == "__main__":
    main()
