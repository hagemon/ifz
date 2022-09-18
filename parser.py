import json
from widget import Widget, WidgetTree, WidgetNode
from executor import executor


def parse_devices_list(device_list, target):
    devices = device_list.split('\n')
    for d in devices:
        info = d.split('|')
        device_name = info[0].strip()
        if device_name == target.value:
            udid = info[1].strip()
            status = info[2].strip()
            version = info[4].strip()
            return {
                'udid': udid,
                'status': status,
                'version': version
            }
    raise Exception('Device: {} has not been installed'.format(target))


def parse_widgets(widgets_str):
    widgets_dict = json.loads(widgets_str)
    widgets = sorted([Widget(d) for d in widgets_dict])
    return widgets


def parse_tab_view(widget_str):
    tab_dict = json.loads(widget_str)
    tab = Widget(tab_dict)
    return tab


def parse_widget_tree(widgets):
    nodes = [WidgetNode(w)for w in widgets]
    root = nodes[0]
    tree = WidgetTree(root)
    hit = [False for _ in range(len(nodes))]
    hit[0] = True
    build_tree(root, nodes, hit, 1)
    tree.print_tree()
    return tree


def build_tree(root, nodes, hit, index):
    for i in range(index, len(nodes)):
        node = nodes[i]
        if not hit[i] and root.widget.contains(node.widget):
            hit[i] = True
            if root.widget.is_group:
                root.childs.append(build_tree(node, nodes, hit, i+1))

    return root
