# import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network
import community as community_louvain


def get_data() -> dict:
    with open(r'data/entity', 'r', encoding='utf-8') as file:
        qs = file.read().splitlines()
    data = {(item[0], item[2]): item[1] for item in [i.split(',') for i in qs]}
    return data


def get_html(edge_to_label: dict) -> None:
    Edge = nx.from_edgelist(edge_to_label.keys())
    communities = community_louvain.best_partition(Edge)
    nx.set_node_attributes(Edge, communities, 'group')
    nt = Network(width='2000px', height='1000px', bgcolor='#222222', font_color='white')
    nt.from_nx(Edge)
    nt.show(name=r'er.html')


def main():
    data = get_data()
    get_html(edge_to_label=data)


if __name__ == '__main__':
    main()
