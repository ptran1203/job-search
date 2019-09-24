import requests
import json
import threading
hook_url = 'https://hooks.slack.com/services/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'


def send(msg):
    requests.post(hook_url, data=json.dumps({'text': msg}))

def send_as_thread(msg):
    thr = threading.Thread(target=send, args=(msg,), kwargs={})
    thr.start()