from checks import loadCheck
from configparser import ConfigParser
from threading import Thread
from time import sleep
from signal import signal, SIGINT, SIGTERM
from os import listdir
from os.path import join
from .http import start_server, stop_server

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

def stop_all_v():
    print('Stopping checker...')
    stop_all()

def stop_all_sigh(_a, _b):
    stop_server()
    stop_all_v()

def stop_all():
    global threads
    for check in checks:
        check.stop_loop()
    for t in threads:
        t.join()
    threads = []

start_all()

start_server()
stop_all_v()

signal(SIGINT, stop_all_sigh)
signal(SIGTERM, stop_all_sigh)
