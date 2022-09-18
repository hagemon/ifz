from abc import ABC, abstractmethod
from app import App
from action import tap
import random


def action_decorator(func):
    def wrapper(_, app: App):
        func(_, app)
        app.get_widgets()
    return wrapper


class Fuzzing(ABC):
    @action_decorator
    @abstractmethod
    def action(self, app: App):
        """
        Doing action with the status of app, like widget_tree and executable_widgets
        :param app:
        :return:
        """
        pass


class RandomFuzzing(Fuzzing):
    @action_decorator
    def action(self, app: App):
        executable = app.executable_widgets
        index = random.randint(0, len(executable))
        w = executable[index]
        tap(w.center.x, w.center.y, app.udid)
