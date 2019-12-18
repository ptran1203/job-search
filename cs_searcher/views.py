from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  JsonResponse, HttpResponse, Http404
from django.views import View
from django.utils import timezone
from django.core import serializers
from django.shortcuts import redirect
from post.models import Post
from searcher.services import search_result
from spider.models import SpiderReport

import numpy as np

def top_page(request):
    template_name = 'index.html'
    docs = Post.objects.all()[:5]
    
    return render(
        request, template_name,
        context={'docs':docs})


def search_view(request):
    query = request.GET.get('q')
    posts = search_result(query) if query else []
    return render(
        request, 'search.html',
        context={'posts': posts}
    )

def report(request):
    access_key = request.GET.get('k')
    if access_key != 'sad03121':
        return render(request, '404.html')
    records = SpiderReport.objects.all().order_by('-run_at')
    return render(
        request, 'report.html',
        context={'records': records}
    )

# error page
def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)