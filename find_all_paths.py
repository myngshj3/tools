import networkx as nx
import re
import sys


def load_diedges(filename):
    with open(filename, 'r') as f:
        edges = []
        while True:
            line = f.readline()
            # print(line)
            if not line:
                break
            result = re.match("(e[0-9]+):(v[0-9]+),(v[0-9]+)", line)
            if result:
                edge = result.group(1)
                node1 = result.group(2)
                node2 = result.group(3)
                edges.append([node1, node2])
            else:
                print("Invlaid format:{}". format(line))
        return edges


def print_diedges(edges):
    for e in edges:
        print("({},{})".format(e[0], e[1]))


if __name__ == "__main__":
    # command = sys.argv[1]
    filename = sys.argv[1]
    start_node = sys.argv[2]
    end_node = sys.argv[3]
    edges = load_diedges(filename)
    # print_diedges(edges)
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e[0], e[1])
    # for e in G.edges:
    #     print("({}, {})".format(e[0], e[1]))
    paths = nx.all_simple_paths(G, start_node, end_node)
    # print("path from {} to {}".format(start_node, end_node))
    for p in paths:
        print(p)

