import random
from executor import executor
from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def apply(self, widget, udid, strategy):
        pass


class Tap(Action):
    def apply(self, widget, udid, strategy=None):
        return executor.tap(widget.center.x, widget.center.y, udid)


class Swipe(Action):
    def apply(self, widget, udid, strategy):
        """
        Apply swipe operation
        :param widget: target widget
        :param udid: device under test
        :param strategy: specific swipe direction within "left", "right", "up", "down" and "random", default "random"
        :return:
        """
        offset_x, offset_y = widget.width // 4, widget.height // 4
        offsets = {
            'left': [offset_x, 0, -offset_x, 0],
            'right': [-offset_x, 0, offset_x, 0],
            'up': [0, -offset_y, 0, offset_y],
            'down': [0, offset_y, 0, -offset_y]
        }
        center = widget.center
        points = center.x, center.y, center.x, center.y
        if strategy == 'random':
            strategy = random.choice(['left', 'right', 'up', 'down'])
        x1, y1, x2, y2 = [points[i]+offsets[strategy][i] for i in range(4)]
        return executor.swipe(int(x1), int(y1), int(x2), int(y2), udid)
