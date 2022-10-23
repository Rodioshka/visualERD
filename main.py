import networkx as nx
from networkx import DiGraph
from pyvis.network import Network
from core.louvain.community_louvain import best_partition
# from core.change_html_file import add_html_parse

from core.service import get_information_db


def get_columns_in_html(data: dict) -> dict:
    list_html = []
    for item, value in data.items():
        list_html.append(
            """<table><thead><tr><th>| Column name</th><th>| Column type</th><th>| Is nullable</th></tr></thead><tbody>""")
        for ke in value:
            list_html.append('<tr>')
            for k, i in ke.items():
                list_html.append(f"""<td>| {k}</td><td>| {i[1]}</td><td>| {i[0]}</td>""")
            list_html.append('</tr>')
        list_html.append("""</tbody></table>""")
        data[item] = ''.join(list_html)
        list_html.clear()
    return data


def reformat_tables_info_for_graph():
    relationships = []
    tables = []
    data = get_information_db()
    for table in data[0][0]:
        # print(table)
        tables.append(table['table_name'])
        for column in table['columns']:
            if column['col_with_foreign'] != '-':
                relationships.append((table['table_name'], column['second_table_name']))
    return tables, relationships


# def get_data_from_db() -> (dict, defaultdict):
#     qs = get_table_with_columns()
#     relationships = dict()
#     info_tables = defaultdict(list)
#     mapa = set()
#
#     for item in get_table_with_foreign_keys():
#         relationships[(item['table_name'], item['foreign_table_name'])] = item['column_name']
#
#     for item in qs:
#         mapa.add(item['table_name'])
#     for m in mapa:
#         for item in qs:
#             if m == item['table_name']:
#                 info_tables[m].append({item['column_name']: [item['is_nullable'], item['data_type']]})
#                 # info_tables[m].append(f"""<tr><td>{item['column_name']}</td><td>{item['data_type']}</td><td>{item['is_nullable']}</td></tr>""")
#     return relationships, info_tables


def get_data() -> dict:
    with open(r'data/entity', 'r', encoding='utf-8') as file:
        qs = file.read().splitlines()
    data = {(item[0], item[2]): item[1] for item in [i.split(',') for i in qs]}
    return data


def get_html(tables: dict, relations: dict) -> None:
    edges = list(relations.keys())
    Edge = DiGraph()
    Edge.add_edges_from(edges)
    for i in tables:
        Edge.add_node(i,
                      title=tables[i])
    communities = best_partition(Edge, weight='weight')
    nx.set_node_attributes(Edge, communities, 'group')
    nt = Network(width='2000px', height='1000px', bgcolor='#222222', font_color='white', directed=True,
                 select_menu=True)
    nt.from_nx(Edge)
    nt.show(name=r'test.html')


def test(tables: dict, relations: dict) -> None:
    pass


def main():
    # relations, tables = get_data_from_db()
    tables, relations = reformat_tables_info_for_graph()
    print(tables)
    # table_with_html_columns = get_columns_in_html(data=tables)
    get_html(tables=tables, relations=relations)
    # add_html_parse(filename='test')


if __name__ == '__main__':
    main()
