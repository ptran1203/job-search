import threading
import requests
import subprocess

SIX_HOURS = 21600
HOST_URL = "http://jsearcher-api.herokuapp.com/"


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

# use later
def ping():
    r = requests.get(HOST_URL + 'api/keywords')

def run_spider():
    subprocess.call(['python', 'spider/core.py'])

def build_vectorspace():
    r = requests.get(HOST_URL + 'api/vectorspace')

# export
def start_scheduler(time_interval=SIX_HOURS/2):
    set_interval(run_spider, time_interval)
    set_interval(build_vectorspace, time_interval + 6000)
    set_interval(ping, 2500)