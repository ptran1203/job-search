from django.shortcuts import render
from post.models import Post
from django.http import (
    HttpResponseRedirect, Http404,
    JsonResponse, HttpResponse
)
from django.views.decorators.csrf import csrf_exempt
from .models import Keywords, VectorSpace
from django.core import serializers
from helper import slack, pagination
from .services import search_result
import constant
from cache import cache
import time


def buildVS(request):
    try:
        now = time.time()
        V = VectorSpace()
        running_time = round(time.time() - now, 2)
        slack.send('build vectorspace successfully, size =%s, done in %s sec' \
                                %(str(V.size), running_time))

        return JsonResponse({
            "status": "Done",
            "size": V.size,
            "time": running_time,
            })
    except Exception as e:
        slack.send(e)
        return JsonResponse({
            "status": "Error!",
            "size": 0
            })


def search(request):
    query = request.GET.get('q')
    page = int(request.GET.get('page') or 0)
    if not query:
        return HttpResponse("no query")

    if not constant.CACHE:
        data = search_result(query)
        if page > 0:
            data = pagination.sub(data, page)
        return JsonResponse(data, safe=False)

    data = cache.get(request)
    if not data:
        data = search_result(query)
        cache.store(request, data)

    return JsonResponse(pagination.sub(data, page), safe=False)

def keywords(request):
    is_string = request.GET.get('is_string')
    # sort_type= str(request.GET.get('sort_type') or 1)
    query_set = Keywords.objects.all().order_by('-num_of_searches')
    if not is_string:
        return JsonResponse([
            item.json_object() for item in query_set
        ], safe=False)
    return JsonResponse([
        item.word for item in query_set
    ], safe=False)

# gg api key: AIzaSyAIlPTH75veCC1TA7ajzt6JDxk3iIonTOc