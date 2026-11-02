# -------------------------------------------------------------------------|--

# UPORABA KNJIŽNICE NETWORKX.READWRITE 

# ZAPISOVANJE NETWORKX GRAFOV V JSON DATOTEKE 

#                \MODELX\NAME_RW.JSON

# ---- from networkx.readwrite import json_graph ----


import json
from networkx.readwrite import json_graph
import os
from pathlib import Path


# -------------------------------------------------------------------------|--


def data_to_RWjson(model_dir, data, name):
    pth = os.path.join(model_dir, f'{name}_RW.json')
    with open(pth, 'w', encoding='utf-8') as g:
        g.write(json.dumps(data, indent=4))


def nx_to_RWjson(model_dir, h, name):
    h_serial_data = json_graph.node_link_data(h)
    data_to_RWjson(model_dir, h_serial_data, name)


def nxnx_to_RWjson(model_dir, hh, name):
    hh_serial = [json_graph.node_link_data(h) for h in hh]
    data_to_RWjson(model_dir, hh_serial, name)


# -------------------------------------------------------------------------|--


def RWjson_to_data(model_dir, name):
    pth = os.path.join(model_dir, f'{name}_RW.json')
    pth = Path(pth)
    if not pth.exists():
        return None
    with open(pth, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def RWjson_to_nx(model_dir, name):
    data = RWjson_to_data(model_dir, name)
    if data is None:
        return None
    h = json_graph.node_link_graph(data)
    return h


def RWjson_to_nxnx(model_dir, name):
    datadata = RWjson_to_data(model_dir, name)
    if datadata is None:
        return None
    hh = [json_graph.node_link_graph(data) for data in datadata]
    return hh


# -------------------------------------------------------------------------|--
