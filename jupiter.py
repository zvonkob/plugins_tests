"""
    SPREHOD ŠIRINO
        IN 
    SPREHOD V GLOBINO
        PO
    NETWORKX.DIGRAPH()
"""


from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import RWjson


m_max, n_max = 2, 3


def main():
    
    h, sw_width = get_input("inputs")

    cTP(h)

    wwidth = walk_digraph(h, sw_width)

    wenumerate(h, wwidth)

    m, n = m_times_n(h, h.cTP)

    # pprint(h)
    # draw_figure(h)

    print(f"\nm_max = {m_max}\nn_max = {n_max}")
    
    hh = []
    
    while True:
    
        g = limit_number_of_sons(h, n_max)

        hh.append(g)
        
        h = subtract(h, g)
        
        if len(h) == 0:
            break

        cTP(h)

        m, n = m_times_n(h, h.cTP)

    wlist = []
    for h in hh:
        # pprint(h)
        wlist.append({
                h["w"]: (h["m"], h["n"])
        })
        break

    for row in wlist:
        w, (m, n) = row
        print(f"{w}: ({m}, {n})")

    draw_figure(h)




def get_input(pth):
    """prebere omrežje"""
    files = []
    for file in Path(pth).iterdir():
        if not file.is_file(): continue
        if file.suffix != ".json": continue
        if not file.stem.endswith("_RW"): continue
        files.append(file)
    # i, sw_width = get_input_input(files)
    i, sw_width = 4, True
    file = files[i-1]
    h = RWjson.RWjson_to_nx(file.parent, file.name[:-8])
    return h, sw_width


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
    print("    1. width first")
    print("    2. depth first")
    while True:
        try:
            j = int(input("Izberi številko: "))
            if j == 1: sw_width = True; break
            if j == 2: sw_width = False; break
            raise ValueError
        except ValueError:
            continue
    print(f"    j = {j}, sw_width = {sw_width}")
    return i, sw_width

 
def cTP(h):
    for id in h.nodes():
        if h.in_degree(id) == 0:
            h.cTP = id; break
    print(f"\ncTP = {h.cTP}")


def walk_digraph(h, sw_width=True):
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


def wenumerate(h, wwidth):
    for i, w in enumerate(wwidth):
        q = h.nodes[w]
        q['w'] = i + 1
    for vid1, vid2, qq in h.edges(data=True):
        q = h.nodes[vid2]
        qq["w"] = q["w"]
    print(f"nodes = {h.number_of_nodes()}")
    print(f"edges = {h.number_of_edges()}")


def m_times_n(h, c):
    if h.out_degree(c) == 0:
        m, n = 0, 1
    else:
        m, n = 0, 0
        for d in h.successors(c):
            md, nd = m_times_n(h, d)
            if md > m: m = md
            n += nd
        m += 1
    h.nodes[c]["m"], h.nodes[c]["n"] = m, n
    return m, n


def pprint(h):
    print()
    for vid, q in h.nodes(data=True):
        w, m, n = q["w"], q["m"], q["n"]
        print(f"{vid} w{w:03d} {m}x{n}")


def limit_number_of_sons(h, n_max):
    g = nx.DiGraph()
    cTP = h.cTP
    g.cTP = cTP
    TODO = [ cTP ]
    while TODO:
        c = TODO.pop()
        q = h.nodes[c]
        qx = q.copy()
        g.add_node(c, **qx)
        for i, d in enumerate(h.successors(c)):
            if i >= n_max:
                continue
            TODO.append(d)
            qq = h.edges[c, d]
            qqx = qq.copy()
            g.add_edge(c, d, **qqx)
    m, n = m_times_n(g, cTP)
    return g


# def do_max_width(h, n_max):
    # g = nx.DiGraph()
    # cTP = h.cTP 
    # TODO = [ cTP ]
    # deleted = []
    # while TODO:
        # c = TODO.pop()
        # q = h.nodes[c]
        # qx = q.copy()
        # g.add_node(c, **qx)
        # for i, d in enumerate(h.successors(c)):
            # if i >= n_max:
                # continue
            # TODO.append(d)
            # qq = h.edges[c, d]
            # qqx = qq.copy()
            # g.add_edge(c, d, **qqx)
            # deleted.append((c, d))
    # m, n = m_times_n(g, cTP)
    # h.remove_edges_from(deleted)
    # deleted = []
    # for c in h.nodes():
        # if h.degree[c] == 0:
            # deleted.append(c)
    # h.remove_nodes_from(deleted)
    # return g


def subtract(h, g):
    # diff = copy.deepcopy(h)
    diff = h.copy()
    diff.remove_edges_from(g.edges())
    diff.remove_nodes_from(list(nx.isolates(diff)))
    return diff
   

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
