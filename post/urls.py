from django.contrib import admin
from django.urls import path, re_path
from .apis import(
    store_post,
    detail,
    count,
    posts,
)

app_name = "post"

urlpatterns = [
    path('store', store_post),
    path('post/<id>', detail),
    path('count', count),
    path('posts', posts)
]
