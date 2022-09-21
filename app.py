from executor import executor
import parser


class App:
    def __init__(self, name, udid):
        self.name = name
        self.udid = udid
        self.widgets = []
        self.executable_widgets = []
        self.widget_tree = None
        self.n_nodes = 0
        self.tracer = []

    def get_widgets(self):
        widgets_str = executor.get_current_ui(udid=self.udid)
        widgets_dict = parser.parse_widgets_dict(widgets_str)
        widgets_tree = parser.parse_widget_tree(widgets_dict)
        self.check_bars(widgets_tree.root)
        # widgets_tree.print_tree()
        self.widget_tree = widgets_tree
        self.executable_widgets = []
        self.get_executable_widgets(widgets_tree.root)

    def check_bars(self, root):
        """
        Tab bar items currently not supported in `idb ui describe-all --nested`,
        one should manually detect these items through `idb ui describe-tap`.
        :param root:
        """
        def check_layer_tabs(node):
            for c in node.childs:
                w = c.widget
                if w.widget_type == 'Group' and not w.has_child:
                    first_tab_str = executor.get_ui_at(w.x + 10, w.y + 10, self.udid)
                    ft_node = parser.parse_tab_view(first_tab_str)
                    ft = ft_node.widget
                    c.childs.append(ft_node)
                    n_items = w.width // ft.width
                    for i in range(1, n_items):
                        tab_srt = executor.get_ui_at(ft.center.x + i * ft.width, ft.center.y, self.udid)
                        t_node = parser.parse_tab_view(tab_srt)
                        c.childs.append(t_node)
                else:
                    for cc in c.childs:
                        check_layer_tabs(cc)
        check_layer_tabs(root)

    def get_executable_widgets(self, root):
        if root.widget.executable:
            self.executable_widgets.append(root.widget)
        for c in root.childs:
            self.get_executable_widgets(c)

    @property
    def is_launched(self):
        return parser.parse_app_status(executor.ls_apps(self.udid), self.name)

    def __str__(self):
        return self.name

    def trace(self, cmd):
        self.tracer.append(cmd+'\n')
