import os
import networkx as nx
from collections import defaultdict
from itertools import combinations
import json
from subprocess import check_call


def notebook2py(notebook_path, py_path):
    """
    Convert jupyter notebook to python script
    """
    check_call(['jupyter', 'nbconvert', '--to', 'script', '--output ', py_path, notebook_path])


def ids2graph(ids2node):
    G = nx.Graph()
    for id in ids2node:
        for node1, node2 in combinations(ids2node[id], 2):
            if not G.has_edge(node1, node2):
                G.add_edge(node1, node2, attr_dict=dict(weight=1, idenifiers=[id]))
            else:
                G[node1][node2]["weight"] += 1
                G[node1][node2]["idenifiers"].append(id)
    return G


def save_graph(graph, filepath):
    nx.write_gml(graph, filepath)

if __name__ == '__main__':
    ids2node = {
        "id1": [1, 2, 3],
        "id2": [2, 3, 4],
        "id3": [4, 5, 6],
        "id4": [6, 7],
        "id5": [7],
    }
    edges = ids2graph(ids2node)
    save_graph(edges, "example.gml")
    G = nx.read_gml("example.gml")
    print(G)
