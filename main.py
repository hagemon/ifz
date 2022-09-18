from device import Device, DeviceType
import yaml

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yaml', 'r'))

    try:
        device = Device(DeviceType.get_name(config['device']))
        device.boot()
        device.launch_app(config['bundles'][0])
    except KeyError as e:
        print('Option {} did not set'.format(e))
