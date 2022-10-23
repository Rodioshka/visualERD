import ast


def add_html_parse(filename):
    with open(fr'{filename}.html') as inf:
        txt = inf.read()

    start = txt.find('nodes = new vis.DataSet')
    end = txt.find('edges = new vis.DataSet')
    lst = (txt[start + 25:end - 22])

    x = ast.literal_eval(lst)

    for i in x:
        i['title'] = f"htmlTitle('{i['title']}')"

    ls = (txt.replace(lst, str(x))).replace('"htmlTitle', 'htmlTitle').replace("""</tbody></table>')"}""",
                                                                               "</tbody></table>')}").replace('([({',
                                                                                                              '([{').replace(
        '})]);', '}]);')

    with open(fr'{filename}.html', 'w') as f:
        f.write(ls)


with open(fr'../test.html') as inf:
    txt = inf.read()

with open(r'../lib/vis-9.0.4/vis-network.css') as f:
    vis_network_css = f.read()

with open(r'../lib/vis-9.0.4/vis-network.min.js') as f:
    vis_network_js = f.read()

with open(r'../lib/tom-select/tom-select.css') as f:
    tom_select_css = f.read()

with open(r'../lib/tom-select/tom-select.complete.min.js') as f:
    tom_select_js = f.read()

with open(r'../lib/bindings/utils.js') as f:
    bindings = f.read()

old_vis_css = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/dist/vis-network.min.css" integrity="sha512-WgxfT5LWjfszlPHXRmBWHkV2eceiWTOBvrKCNbdgDYTHrT2AeLCGbF4sZlZw3UMN3WtL0tGUoIAKsu8mllg/XA==" crossorigin="anonymous" referrerpolicy="no-referrer" />'
new_vis_css = txt.replace(old_vis_css, f'<style>{vis_network_css}</style>')

old_vis_js = '<script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.2/dist/vis-network.min.js" integrity="sha512-LnvoEWDFrqGHlHmDD2101OrLcbsfkrzoSpvtSQtxK3RMnRV0eOkhhBN2dXHKRrUU8p2DGRTk35n4O8nWSVe1mQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'
new_vis_js = new_vis_css.replace(old_vis_js, f'<script>{vis_network_js}</script>')

old_tom_css = '<link href="lib/tom-select/tom-select.css" rel="stylesheet">'
new_tom_css = new_vis_js.replace(old_tom_css, f'<style>{tom_select_css}</style>')

old_tom_js = '<script src="lib/tom-select/tom-select.complete.min.js"></script>'
new_tom_js = new_tom_css.replace(old_tom_js, f'<script>{tom_select_js}</script>')

old_bindings = '<script src="lib/bindings/utils.js"></script>'
new_bindings = new_tom_js.replace(old_bindings, f'<script>{bindings}</script>')


with open(fr'../test.html', 'w') as file:
    file.write(new_bindings)