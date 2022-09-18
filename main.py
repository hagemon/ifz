from device import Device
import yaml
from fuzzing import RandomFuzzing

if __name__ == '__main__':
    config = yaml.safe_load(open('config.yaml', 'r'))

    try:
        device = Device(config['device'])
        device.boot()
        device.launch_app(config['bundle'])
        fuzz = RandomFuzzing()
        for _ in range(1):
            fuzz.action(device.active_app)
    except KeyError as e:
        print('Option {} did not set'.format(e))
