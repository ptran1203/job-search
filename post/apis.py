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
