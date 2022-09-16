from executor import executor
import parser
import random


class App:
    def __init__(self, name):
        self.name = name
        self.widgets = []
        self.executable_widgets = []

    def get_widgets(self):
        widgets_str = executor.get_current_ui()
        widgets = parser.parse_widgets(widgets_str)
        self.widgets = widgets
        self.executable_widgets = [w for w in widgets if w.widget_type == 'Button']

    def random_tap(self):
        ind = random.randint(0, len(self.executable_widgets)-1)
        chosen = self.executable_widgets[ind]
        executor.tap(chosen.center[0], chosen.center[1])
