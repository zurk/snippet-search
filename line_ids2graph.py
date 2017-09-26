import os
import argparse
import networkx as nx
import igraph as ig
from collections import defaultdict
from itertools import combinations
import json
from subprocess import check_call
import sys

def get_cuts(ids2node, lines_num):
    cuts = [0] * (lines_num - 1)

    for id in ids2node:
        lines = sorted(ids2node[id])
        n = len(lines)
        for i in range(len(lines)-1):
            for j in range(lines[i]-1, lines[i+1]-1):
                cuts[j] += (n - 1 - i) * (i + 1)
    return cuts


def cuts2snippets(cuts):
    snippets = [[1, 0]]
    down = False
    eq = False
    k = 0
    for i in range(len(cuts)-1):
        k += 1
        if cuts[i+1] > cuts[i]:
            if (down or eq) and k >= 5:
                k = 0
                snippets[-1][1] = i
                snippets.append([i+1, 0])
            down = False
            eq = False
        if cuts[i + 1] < cuts[i]:
            down = True
        if cuts[i + 1] == cuts[i]:
            eq = True
    snippets[-1][1] = len(cuts) + 1
    return snippets


def notebook2py(notebook_path):
    """
    Convert jupyter notebook to python script
    """
    check_call(['jupyter', 'nbconvert', '--to', 'script', notebook_path])


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
    parser.add_argument('--experiment-mode', action="store_true", default=False)
    parser.add_argument('--input', default=None, required=False)
    parser.add_argument('--output', default=None, required=False)
    args = parser.parse_args()
    if args.experiment_mode:
        input = args.input
        if args.input.endswith(".ipynb"):
            notebook2py(input)
            input = input.replace(".ipynb", ".py")
        ids = get_ids(args.input)
        lines_num = max([max(lines) for lines in ids.values()])
        cut = get_cuts(ids, lines_num=lines_num)
        res = cuts2snippets(cut)
        json.dump(convert2json(res), open(args.output, 'w'))
        print(res)
    else:
        ids = json.load(sys.stdin)
        lines_num = max([max(lines) for lines in ids.values()])
        cut = get_cuts(ids, lines_num=lines_num)
        res = cuts2snippets(cut)
        sys.stdout.write(json.dumps(convert2json(res)))

        ids = json.load(sys.stdin)
        lines_num = max([max(lines) for lines in ids.values()])
        cut = get_cuts(ids, lines_num=lines_num)
        res = cuts2snippets(cut)
        sys.stdout.write(json.dumps(convert2json(res)))
