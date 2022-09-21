from subprocess import Popen, PIPE
from threading import Lock
import logger
import time


def execution_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
            exit(1)
    return wrapper


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Executor(metaclass=Singleton):

    @staticmethod
    def _execute(cmd, udid):
        # print(cmd)
        with Popen(args=cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8') as p:
            result = p.stdout.read()
            err = p.stderr.read()
            if len(err) > 0:
                logger.log_err(err, udid, cmd)
                raise ConnectionError(err)
            return result

    def ls_device(self):
        devices = self._execute('idb list-targets', '')[:-1]
        return devices

    def connect_device(self, udid):
        self._execute('idb connect {}'.format(udid), udid)

    def ls_apps(self, udid):
        apps = self._execute('idb list-apps --udid {}'.format(udid), udid)
        return apps

    def boot_device(self, udid):
        self._execute('idb boot {}'.format(udid), udid)
        logger.log('Successfully booting simulator {}'.format(udid))
        time.sleep(0.5)

    def home(self, udid):
        self._execute('idb ui button HOME --udid {}'.format(udid), udid)
        time.sleep(0.5)

    def launch_app(self, udid, app):
        log = self._execute('idb launch --udid {} {}'.format(udid, app), udid)
        # logger.log('Successfully launching app {}'.format(app))
        logger.log(log)
        time.sleep(3)

    def terminate_app(self, udid, app):
        try:
            log = self._execute('idb terminate --udid {} {}'.format(udid, app), udid)
            logger.log(log)
            time.sleep(1.5)
        except ConnectionError as _:
            print('{} has been terminated in {}'.format(app, udid))

    def get_current_ui(self, udid):
        views = self._execute('idb ui describe-all --udid {} --nested'.format(udid), udid)
        return views

    def get_ui_at(self, x, y, udid):
        view = self._execute('idb ui describe-point {} {} --udid {}'.format(x, y, udid), udid)
        return view

    def tap(self, x, y, udid):
        cmd = 'idb ui tap {} {} --udid {}'.format(x, y, udid)
        self._execute(cmd, udid)
        logger.log('tap {} {} udid: {}'.format(x, y, udid))
        time.sleep(1)
        return cmd

    def swipe(self, x1, y1, x2, y2, udid):
        cmd = 'idb ui swipe {} {} {} {} --udid {}'.format(x1, y1, x2, y2, udid)
        self._execute(cmd, udid)
        logger.log('swipe {} {} to {} {} udid: {}'.format(x1, y1, x2, y2, udid))
        time.sleep(1)
        return cmd


executor = Executor()
