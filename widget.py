class Widget:
    def __init__(self, widget_dict):
        frame = widget_dict['frame']
        self.x = frame['x']
        self.y = frame['y']
        self.width = frame['width']
        self.height = frame['height']
        self.center = (int(self.x+0.5*self.width), int(self.y+0.5*self.height))
        self.role = widget_dict['role_description']
        self.label = widget_dict['AXLabel']
        self.widget_type = widget_dict['type']


class WidgetNode:
    def __init__(self, widget):
        self.widget = widget
        self.parent = None
        self.childs = []


class WidgetTree:
    pass
