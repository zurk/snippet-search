import os
import argparse
import networkx as nx
import igraph as ig
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


def convert2json(comms):
    to_ui = []
    for i, comm in enumerate(comms):
        to_ui.append(dict(
            key="snippet{}".format(i),
            pos=(min(comm), max(comm)),
            content=None
        ))
        
    return to_ui


def get_snippets(filepath):
    # 1. convert gml file to graph:
    g = ig.Graph.Read_GML(filepath)
    # 2. detect communities:
    communities = g.community_walktrap()
    # 3. convert the communities to clusters:
    clusters = communities.as_clustering()
    # 4. extract list of communities:
    L = list(clusters)
    # 5. convert to json:
    return convert2json(L)


def save_nx_graph(graph, filepath):
    nx.write_gml(graph, filepath)


def load_igraph(filepath):
    return nx.read_gml("example.gml")

def get_ids(filepath, lang="python"):
    outfile = 'data/ids_out.json'
    check_call(['go', 'run', 'identifiers-extractor.go', '-file', filepath, '-lang', lang,
                '-out', outfile])
    return json.load(open(outfile))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Snippet detection tool.')
    parser.add_argument('input')
    parser.add_argument('output')

    args = parser.parse_args()
    ids = get_ids(args.input)
    edges = ids2graph(ids)
    save_nx_graph(edges, "data/graph.gml")
    snippets = get_snippets("data/graph.gml")
    print(snippets)
    json.dump(snippets, open(args.output, "w"))
