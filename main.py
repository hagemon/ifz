from device import Device
from fuzzing import RandomFuzzing
import yaml
from multiprocessing import Process
import logger


def run(device, apps):
    try:
        device = Device(device)
        device.boot()
        device.home()
        for app in apps:
            device.launch_app(app)
            fuzz = RandomFuzzing()
            for _ in range(20):
                try:
                    fuzz.action(device.active_app)
                except RuntimeError as e:
                    logger.log(e)
                    logger.log_crash(e, device.active_app)
                    break
    except KeyError as err:
        print('Option {} did not set'.format(err))


if __name__ == '__main__':
    config = yaml.safe_load(open('config.yaml', 'r'))
    targets = config['targets']
    for t in targets:
        p = Process(target=run, args=(t, targets[t]))
        p.start()


