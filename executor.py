from subprocess import Popen, PIPE
from threading import Lock
import logger
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Executor(metaclass=Singleton):

    @staticmethod
    def _execute(cmd):
        print(cmd)
        with Popen(args=cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8') as p:
            result = p.stdout.read()
            return result

    def ls_device(self):
        devices = self._execute('idb list-targets')[:-1]
        return devices

    def ls_apps(self, udid):
        apps = self._execute('idb list-apps --udid {}'.format(udid))
        return apps

    def boot_device(self, udid):
        self._execute('idb boot {}'.format(udid))
        logger.log('Successfully booting simulator {}'.format(udid))
        time.sleep(0.5)

    def home(self, udid):
        self._execute('idb ui button HOME --udid {}'.format(udid))
        time.sleep(0.5)

    def launch_app(self, udid, app):
        log = self._execute('idb launch --udid {} {}'.format(udid, app))
        # logger.log('Successfully launching app {}'.format(app))
        logger.log(log)
        time.sleep(3)

    def terminate_app(self, udid, app):
        log = self._execute('idb terminate --udid {} {}'.format(udid, app))
        logger.log(log)
        time.sleep(1.5)

    def get_current_ui(self, udid):
        views = self._execute('idb ui describe-all --udid {} --nested'.format(udid))
        if len(views) == 0:
            raise Exception('Connection Refused on {}'.format(udid))
        return views

    def get_ui_at(self, x, y, udid):
        view = self._execute('idb ui describe-point {} {} --udid {}'.format(x, y, udid))
        return view

    def tap(self, x, y, udid):
        # self._execute('idb ui tap {} {} --udid {}'.format(x, y, udid))
        self._execute('idb ui tap 357 69 --udid {}'.format(udid))
        # logger.log('tap {} {} udid: {}'.format(x, y, udid))
        time.sleep(1)


executor = Executor()
