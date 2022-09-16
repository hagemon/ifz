import json
from widget import Widget


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
    widgets = [Widget(d) for d in widgets_dict]
    return widgets


def parse_widget_tree(widgets):
    pass
