# from .models import SpiderReport
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from helper import slack
import json
import subprocess

KEY = 'asd56a4s651ca'
SRC_MAP = {1: 'topitworks', 2: 'itviec'}

@csrf_exempt
def store(request):
    """
    Handle post request from crawler
    """
    if request.method != 'POST':
        return HttpResponse("please correct your request")

    data = json.loads(request.body.decode('utf8'))
    # new = SpiderReport(
    #     running_time = data['running_time'] or 0,
    #     crawled_pages = data['crawled_pages'] or 0,
    #     src_type = data['src_type'] or 0,
    # )
    # new.save()
    return HttpResponse("Ok")

def start_crawler(request):
    key = request.GET.get('k')
    src_id = int(request.GET.get('src'))
    site = SRC_MAP[src_id]
    if not site or key != KEY:
        raise Http404

    pipe = subprocess.Popen(['python', 'spider/core.py', site])
    slack.send('You have start crawler manually for `' + site + '`')
    return JsonResponse({'status': 'started'})
