from django.shortcuts import render
from .models import TechTalk
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse

# Create your apis here.

def crawl(request):
    TechTalk().save()
    return HttpResponse("1")