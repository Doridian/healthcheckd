from checks import loadCheck
from configparser import ConfigParser
from threading import Thread
from os import listdir
from os.path import join

parser = ConfigParser()

config_dir = 'config'
for f in listdir(config_dir):
    if f[0] != '.':
        print('Reading config file %s' % f)
        parser.read(join(config_dir, f))

checks = []

for section_name in parser.sections():
    section = parser[section_name]
    section['name'] = section_name
    checks.append(loadCheck(section))

threads = []

def is_all_up():
    for check in checks:
        if not check.is_up():
            return False
    return True

def start_all():
    global threads
    stop_all()
    for check in checks:
        t = Thread(name='Check %s' % check.name, daemon=True, target=check.run_loop)
        t.start()
        threads.append(t)

def stop_all():
    global threads
    for check in checks:
        check.stop_loop()
    for t in threads:
        t.join()
    threads = []