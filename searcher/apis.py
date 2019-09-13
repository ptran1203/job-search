from django.shortcuts import render
from post.models import Post
from django.http import (
    HttpResponseRedirect, Http404,
    JsonResponse, HttpResponse
)
from django.views.decorators.csrf import csrf_exempt
from .models import Keywords
from .vector_space import VectorSpace
from django.core import serializers
from helper import http as httpHelper
from .services import search_result

def buildVS(request):
    try:
        V = VectorSpace()
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

    return httpHelper.json_response(search_result(query))

def keywords(request):
    is_string = request.GET.get('is_string')
    query_set = Keywords.objects.all()
    if not is_string:
        return JsonResponse([
            item.json_object() for item in query_set
        ], safe=False)
    return JsonResponse([
        item.word for item in query_set
    ], safe=False)


## helper
