from checks import loadCheck
from configparser import ConfigParser
from threading import Thread
from time import sleep
from signal import signal, SIGINT, SIGTERM

parser = ConfigParser()
parser.read('config.ini')

checks = []

for section_name in parser.sections():
    section = parser[section_name]
    section['name'] = section_name
    checks.append(loadCheck(section))

threads = []

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
    stop_all_v()

def stop_all():
    global threads
    for check in checks:
        check.stop_loop()
    for t in threads:
        t.join()
    threads = []

start_all()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print('Ctrl-C caught')
    stop_all_v()

signal(SIGINT, stop_all_sigh)
signal(SIGTERM, stop_all_sigh)
