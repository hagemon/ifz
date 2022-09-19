from enum import Enum
from executor import executor
from app import App
import parser
import logger


class DeviceStatus(Enum):
    SHUTDOWN = 'SHUTDOWN'
    BOOTED = 'BOOTED'
    SHUTTING_DOWN = 'SHUTTING DOWN'

    @staticmethod
    def get_name(value: str):
        try:
            return DeviceStatus(value.upper())
        except ValueError as e:
            print('Status {} is not supported'.format(e))
            exit(0)


class Device:
    def __init__(self, device_type):
        self.device_type = device_type

        # Update after boosting
        self.status = DeviceStatus.SHUTDOWN
        self.udid = None
        self.version = None

        self.apps = {}
        self.active_app = None

    def boot(self):
        devices = executor.ls_device()
        info = parser.parse_devices_list(devices, self.device_type)
        if not info:
            print('Device {} is not installed, try to install it or choose one available:'.format(self.device_type))
            print(parser.show_devices_list(devices))
            exit(1)

        self.status = DeviceStatus.get_name(info['status'])
        self.udid = info['udid']
        self.version = info['version']

        if self.status == DeviceStatus.SHUTDOWN:
            executor.boot_device(self.udid)
        else:
            logger.log('Simulator: {} has already been booted'.format(self))

    def home(self):
        executor.home(self.udid)

    def launch_app(self, app_name):
        app_list = executor.ls_apps(self.udid)
        if not parser.check_app_installation(app_list, app_name):
            print('App "{}" has not been installed/compiled on "{}"'.format(app_name, self))
            exit(1)
        executor.terminate_app(self.udid, app_name)
        executor.launch_app(self.udid, app_name)
        app = App(app_name, self.udid)
        self.apps[app_name] = app
        self.active_app = app
        self.get_current_ui()

    def get_current_ui(self):
        if self.active_app:
            self.active_app.get_widgets()

    def apply_fuzzing_action(self):
        pass

    def __str__(self):
        return '{} ({})'.format(self.device_type, self.udid)

