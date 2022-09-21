import time


def log(text):
    print(text)


def log_err(e, udid, cmd):
    with open('log.txt', 'a') as f:
        f.write('udid: {} crash on cmd: {} with err: {}\n'.format(udid, cmd, e))


def log_crash(e, app):
    with open('crashes.txt', 'a') as f:
        dt = time.asctime(time.localtime(time.time()))
        f.write('\ntime: {} udid: {} app: {}\n'.format(dt, app.udid, app))
        f.write('with error: {}\n'.format(e))
        f.write('trace:\n')
        f.writelines(app.tracer)
