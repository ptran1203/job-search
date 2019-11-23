import requests
import json
import threading
import constant
hook_url = 'https://hooks.slack.com/services/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'

def do(msg):
    requests.post(hook_url, data=json.dumps({'text': msg}))

def send(msg):
    if not constant.IS_PROD:
        return
    thr = threading.Thread(target=do, args=(msg,), kwargs={})
    thr.start()
