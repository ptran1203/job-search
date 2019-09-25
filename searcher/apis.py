from django.shortcuts import render
from post.models import Post
from django.http import (
    HttpResponseRedirect, Http404,
    JsonResponse, HttpResponse
)
from django.views.decorators.csrf import csrf_exempt
from .models import Keywords, VectorSpace
from django.core import serializers
from helper import http as httpHelper
from helper import slack
from .services import search_result

def buildVS(request):
    try:
        V = VectorSpace()
        slack.send_as_thread('build vectorspace successfully, size =' + str(V.size))
        return JsonResponse({
            "status": "Done",
            "size": V.size
            })
    except:
        return JsonResponse({
            "status": "Error!",
            "size": 0
            })


def search(request):
    query = request.GET.get('q')
    if not query:
        return HttpResponse("no query")

    return JsonResponse(search_result(query), safe=False)

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