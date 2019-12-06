"""cs_searcher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from .views import (top_page,
                    search_view,
                    report,
                    facial_predict)


apis = [
    path('api/', include('post.urls', namespace='crawler')),
    path('api/', include('searcher.urls')),
    path('api/', include('spider.urls')),
    path('api/facial/score', facial_predict )
]

pages = [
    path('admin/', admin.site.urls),
    path('', top_page),
    path('search', search_view),
    path('report', report),
]

handler404 = 'cs_searcher.views.handler404'

urlpatterns = pages + apis

# start scheduler here

from scheduler.core import start_scheduler

start_scheduler()
