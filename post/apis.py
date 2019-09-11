from django.shortcuts import render
from .models import Post
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
    return JsonResponse(post.json_object(is_html=True))

def count(request):
    """
    Count item in DB
    """
    return JsonResponse({'count': Post.objects.count()})
