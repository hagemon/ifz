import subprocess
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
        return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

    def ls_device(self):
        devices = self._execute('idb list-targets')[:-1]
        return devices

    def ls_apps(self):
        apps = self._execute('idb list-apps')
        print(apps)

    def boot_device(self, udid):
        self._execute('idb boot {}'.format(udid))
        logger.log('Successfully booting simulator {}'.format(udid))

    def launch_app(self, udid, app):
        self._execute('idb launch --udid {} {}'.format(udid, app))
        logger.log('Successfully launching app {}'.format(app))

    def get_current_ui(self):
        views = self._execute('idb ui describe-all')
        return views

    def tap(self, x, y):
        print('tap {} {}'.format(x, y))
        self._execute('idb ui tap {} {}'.format(x, y))
        time.sleep(0.5)


executor = Executor()
