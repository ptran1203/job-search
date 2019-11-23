from django.urls import path, re_path
from .apis import (
    store,
    start_crawler
)

app_name = "spider"

urlpatterns = [
    path('report/store', store),
    path('crawler/start', start_crawler),
]