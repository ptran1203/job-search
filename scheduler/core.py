import threading
import requests
import subprocess
import time
import datetime
from helper import slack
import os
from constant import HOST_URL

one_minute = 60


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

# use later
def ping():
    # do not ping from 3AM to 6AM
    # if (2 < datetime.datetime.now().hour < 7):
    #     slack.send('Server sleeping now...')
    #     return
    r = requests.get(HOST_URL + 'api/keywords')

def run_spider():
    slack.send('start crawler')
    subprocess.call(['python', 'spider/core.py'])
    # clean posts first
    requests.get(HOST_URL + 'api/clean')
    requests.get(HOST_URL + 'api/vectorspace')

def clear_cache():
    path = os.getcwd() + '/cache/storage/'
    for file in os.listdir(path):
        fpath = path + file
        os.path.isfile(fpath) and os.remove(fpath)


# export
def start_scheduler():
    set_interval(run_spider, one_minute * 60 * 7)
    set_interval(ping, one_minute * 27)
    set_interval(clear_cache, one_minute * 60)