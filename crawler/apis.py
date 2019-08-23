from django.shortcuts import render
from .models import Post
from .crawl import Spider
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse


def crawl(request):
    sp = Spider()
    # res = sp.start_requests()
    # for r in res:
    #     print(r)
    # sp.parse(res)

    return HttpResponse("1")