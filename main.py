from device import Device, DeviceType
import yaml

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yaml', 'r'))

    device = Device(DeviceType.get_name(config['device']))
    device.boot()
    device.launch_app(config['bundles'][0])

    for _ in range(10):
        device.random_event()
