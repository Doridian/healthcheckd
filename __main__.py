
from server import start_server, stop_server
from checker import start_all, stop_all
from signal import signal, SIGINT, SIGTERM

def stop_all_v():
    print('Stopping checker...')
    stop_all()

def stop_all_sigh(_a, _b):
    stop_server()
    stop_all_v()

start_all()

start_server(2080)
stop_all_v()

signal(SIGINT, stop_all_sigh)
signal(SIGTERM, stop_all_sigh)
