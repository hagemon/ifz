from enum import Enum
from executor import executor
from app import App
import parser
import logger


class DeviceType(Enum):
    PHONE_11 = 'iPhone 11'
    PHONE_11_P = 'iPhone 11 Pro'
    PHONE_11_PM = 'iPhone 11 Pro Max'
    PHONE_12 = 'iPhone 12'
    PHONE_12_P = 'iPhone 12 Pro'
    PHONE_12_PM = 'iPhone 12 Pro Max'
    PHONE_12_MI = 'iPhone 12 mini'
    PHONE_13 = 'iPhone 13'
    PHONE_13_P = 'iPhone 13 Pro'
    PHONE_13_PM = 'iPhone 13 Pro Max'
    PHONE_13_MI = 'iPhone 13 mini'
    PHONE_14 = 'iPhone 14'
    PHONE_14_P = 'iPhone 14 Pro'
    PHONE_14_PM = 'iPhone 14 Pro Max'
    PHONE_SE = 'iPhone SE (2nd generation)'
    PHONE_8 = 'iPhone 8'
    PHONE_8_P = 'iPhone 8 Plus'

    @staticmethod
    def get_name(value: str):
        return DeviceType(value)


class DeviceStatus(Enum):
    SHUTDOWN = 'SHUTDOWN'
    BOOTED = 'BOOTED'
    SHUTTING_DOWN = 'SHUTTING DOWN'

    @staticmethod
    def get_name(value: str):
        return DeviceStatus(value.upper())


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
        self.status = DeviceStatus.get_name(info['status'])
        self.udid = info['udid']
        self.version = info['version']

        if self.status == DeviceStatus.SHUTDOWN:
            executor.boot_device(self.udid)
        else:
            logger.log('Simulator: {} has already been booted'.format(self.device_type))

    def launch_app(self, app_name):
        app = App(app_name, self.udid)
        executor.launch_app(self.udid, app.name)
        self.apps[app_name] = app
        self.active_app = app
        self.get_current_ui()

    def get_current_ui(self):
        if self.active_app:
            self.active_app.get_widgets()

    def random_event(self):
        if self.active_app:
            print('starting event')
            self.active_app.random_tap()
            self.get_current_ui()


