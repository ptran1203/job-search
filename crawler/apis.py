from django.shortcuts import render
from .models import Post
from .bot import start
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse


def crawl(request):
    start()
    return HttpResponse("1")