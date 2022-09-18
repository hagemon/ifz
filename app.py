from executor import executor
import parser
import random


class App:
    def __init__(self, name, udid):
        self.name = name
        self.udid = udid
        self.widgets = []
        self.executable_widgets = []
        self.widget_tree = None

    def get_widgets(self):
        widgets_str = executor.get_current_ui(udid=self.udid)
        widgets = parser.parse_widgets(widgets_str)
        widgets = self.get_tabs(widgets)
        widgets_tree = parser.parse_widget_tree(widgets)
        self.widgets = widgets
        self.widget_tree = widgets_tree
        self.executable_widgets = [w for w in widgets if w.widget_type == 'Button']
        
    def get_tabs(self, widgets):
        """
        Tab bar items currently not supported in `idb ui describe-all`,
        one should manually detect these items through `idb ui describe-tap`.
        :param widgets: 
        :return: widgets: widget list with tab items
        """
        for w in widgets:
            if w.label == 'Tab Bar':
                first_tab_str = executor.get_ui_at(w.x+10, w.y+10, self.udid)
                ft = parser.parse_tab_view(first_tab_str)
                widgets.append(ft)
                n_items = w.width // ft.width
                for i in range(1, n_items):
                    tab = executor.get_ui_at(ft.center.x + i*ft.width, ft.center.y, self.udid)
                    t = parser.parse_tab_view(tab)
                    widgets.append(t)
        
        return widgets

    def random_tap(self):
        ind = random.randint(0, len(self.executable_widgets)-1)
        chosen = self.executable_widgets[ind]
        executor.tap(chosen.center.x, chosen.center.y, udid=self.udid)

