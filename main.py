import networkx as nx
from networkx import DiGraph
from pyvis.network import Network
from core.louvain.community_louvain import best_partition
from core.change_html_file import add_html_parse

from core.service import get_information_db


def reformat_tables_info_for_graph():
    tables, relationships, list_html = {}, [], []

    data = get_information_db()

    for table in data[0][0]:
        list_html.append(
            """<table><thead><tr><th>| Column name</th><th>| Column type</th><th>| Is nullable</th></tr></thead><tbody>""")
        list_html.append('<tr>')
        for column in table['columns']:
            list_html.append(
                f"""<td>| {column['column_name']}</td><td>| {column['type']}</td><td>| {column['column_name']}</td>""")
            if column['col_with_foreign'] != '-':
                relationships.append((table['table_name'], column['second_table_name']))
        list_html.append('</tr>')
        tables[table['table_name']] = ''.join(list_html)
        list_html.clear()
    return tables, relationships


def get_html_with_graph(tables: dict, relations: list) -> None:
    edge = DiGraph()
    for table_name, columns in tables.items():
        edge.add_node(table_name,
                      title=columns)
    edge.add_edges_from(relations)
    communities = best_partition(edge, weight='weight')
    nx.set_node_attributes(edge, communities, 'group')
    nt = Network(width='2000px', height='1000px', bgcolor='#222222', font_color='white', directed=True,
                 select_menu=True)
    nt.from_nx(edge)
    nt.show(name=r'test.html')


def main():
    tables, relations = reformat_tables_info_for_graph()
    get_html_with_graph(tables=tables, relations=relations)
    add_html_parse(filename='test')


if __name__ == '__main__':
    main()
