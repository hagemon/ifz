from abc import ABC, abstractmethod
from app import App
import random
from action import Tap, Swipe


def action_decorator(func):
    def wrapper(_, app: App):
        cmd = func(_, app)
        app.trace(cmd)
        app.get_widgets()
        if not app.is_launched:
            raise RuntimeError('app: {} crash!'.format(app))
    return wrapper


class Fuzzing(ABC):
    @action_decorator
    @abstractmethod
    def action(self, app: App) -> str:
        """
        Doing action with the status of app, like widget_tree and executable_widgets
        :param app:
        :return: command
        """
        pass


class RandomFuzzing(Fuzzing):
    @action_decorator
    def action(self, app: App):
        executable = app.executable_widgets
        index = random.randint(0, len(executable)-1)
        w = executable[index]
        tap = Tap()
        swipe = Swipe()
        action = random.choice([tap, swipe])
        return action.apply(w, app.udid, strategy='random')
