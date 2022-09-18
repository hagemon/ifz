class Widget:
    def __init__(self, widget_dict):
        frame = widget_dict['frame']
        self.x = frame['x']
        self.y = frame['y']
        self.width = frame['width']
        self.height = frame['height']
        self.center = Point(int(self.x+0.5*self.width), int(self.y+0.5*self.height))
        self.role = widget_dict['role_description']
        self.label = widget_dict['AXLabel']
        self.widget_type = widget_dict['type']
        self.is_group = self.widget_type in ['Group', 'Application']

    def contains(self, other):
        return (self.x + self.width > other.center.x > self.x) and (self.y + self.height > other.center.y > self.y)

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.y
        return self.y < other.y


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class WidgetNode:
    def __init__(self, widget):
        self.widget = widget
        self.parent = None
        self.childs = []

    def append_child(self, node):
        self.childs.append(node)

    def __str__(self):
        return "{} {}".format(self.widget.label, self.widget.widget_type)


class WidgetTree:
    def __init__(self, root):
        self.root = root

    def print_tree(self):
        def print_layer(node, i):
            print('    '*i+'|'+'----'*i, end='')
            print(node)
            for n in node.childs:
                print_layer(n, i+1)

        print_layer(self.root, 0)
