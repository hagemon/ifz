import json
from widget import Widget, WidgetTree, WidgetNode


def parse_devices_list(device_list, target):
    devices = device_list.split('\n')
    for d in devices:
        info = d.split('|')
        device_name = info[0].strip()
        if device_name == target:
            udid = info[1].strip()
            status = info[2].strip()
            version = info[4].strip()
            return {
                'udid': udid,
                'status': status,
                'version': version
            }
    return None


def show_devices_list(device_list):
    devices = device_list.split('\n')
    s = ''
    for d in devices:
        info = d.split('|')
        device_name = info[0].strip()
        device_id = info[1].strip()
        s += '{} | udid: {}\n'.format(device_name, device_id)
    return s


def check_app_installation(app_list, target):
    apps = app_list.split('\n')
    for a in apps:
        info = a.split('|')
        app_name = info[0].strip()
        if app_name == target:
            return True
    return False


def parse_widgets_dict(widgets_str):
    widgets_dict = json.loads(widgets_str)
    return widgets_dict


def parse_tab_view(widget_str):
    tab_dict = json.loads(widget_str)
    tab = Widget(tab_dict)
    tab_node = WidgetNode(tab)
    return tab_node


def parse_widget_tree(widgets_dict):
    def parse_tree_cur(nd):
        n = WidgetNode(Widget(nd))
        for c in nd['children']:
            n.childs.append(parse_tree_cur(c))
        return n

    root_dict = widgets_dict[0]
    root_widget = Widget(root_dict)
    root = WidgetNode(root_widget)
    for node_dict in root_dict['children']:
        node = parse_tree_cur(node_dict)
        root.childs.append(node)
    tree = WidgetTree(root)
    return tree
