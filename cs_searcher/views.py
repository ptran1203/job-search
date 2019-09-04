from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import  JsonResponse, HttpResponse
from django.views import View
from django.utils import timezone
from django.core import serializers
from django.shortcuts import redirect
from post.models import Post

def top_page(request):
    template_name = 'index.html'
    docs = Post.objects.all()[:5]
    
    return render(
        request, template_name,
        context={'docs':docs})


