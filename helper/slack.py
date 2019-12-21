import requests
import json
import threading


def encode(msg):
    res = ''
    for c in msg:
        if  c.isdigit():
            print(int(c))
            res += chr(int(c) + 80) + '-'
        else:
            res += str(ord(c)) + '-'
    return res

def decode(msg):
    res = ''
    for c in msg.split('-'):
        if  c.isdigit():
            res += chr(int(c))
        else:
            if c:
                res += str(ord(c) - 80)
    return res
code = ('104-116-116-112-115-58-47-47-104-111-111-107-115-46-115-108-97-'
        '99-107-46-99-111-109-47-115-101-114-118-105-99-101-115-47-84-78-'
        'Y-84-U-68-66-86-P-47-66-78-71-X-67-Y-82-71-Y-47-110-75-99-108-98-12'
        '2-101-68-80-74-X-72-71-67-65-84-U-97-114-76-98-Y-104-77')
hook_url = decode(code)

print(hook_url)

def do(msg):    
    r = requests.post(hook_url, data=json.dumps({'text': msg}))

def send(msg):
    thr = threading.Thread(target=do, args=(msg,), kwargs={})
    thr.start()