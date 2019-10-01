from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Post

import json

@csrf_exempt
def store_post(request):
    """
    Handle post request from crawler
    """
    if request.method != 'POST':
        return HttpResponse("please correct your request")

    data = json.loads(request.body.decode('utf8'))
    Post.create(data)

    return HttpResponse("Ok")

def detail(request, id):
    """
    Get data for specific post
    """
    post = Post.objects.get(pk=id)
    return JsonResponse(post.json_object())

def count(request):
    """
    Count item in DB
    """
    return JsonResponse({'count': Post.objects.count()})

def posts(request):
    """
    Get posts and sort by condition
    query: ?sort_type=<type>&limit=<limit>
    """
    sort_type = int(request.GET.get('sort_type')) or 1
    limit = int(request.GET.get('limit')) or 15

    sort_map = {
        1: '-id',
        2: 'id',
        3: '-post_date',
        4: 'post_date'
    }

    return JsonResponse([post.json_object() for post in \
            Post.objects.\
            order_by(sort_map[sort_type])[:limit]
    ], safe=False)
