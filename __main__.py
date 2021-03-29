
from .http import start_server, stop_server
from signal import signal, SIGINT, SIGTERM
from .checker import start_all, stop_all

def stop_all_v():
    print('Stopping checker...')
    stop_all()

def stop_all_sigh(_a, _b):
    stop_server()
    stop_all_v()

start_all()

start_server()
stop_all_v()

signal(SIGINT, stop_all_sigh)
signal(SIGTERM, stop_all_sigh)
