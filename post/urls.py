from django.contrib import admin
from django.urls import path, re_path
from .apis import(store_post,detail,count,
                clean,get_posts,
                get_posts_by_query)

app_name = "post"

urlpatterns = [
    path('store', store_post),
    path('posts/<id>', detail),
    path('count', count),
    path('clean', clean),
    path('posts', get_posts),
    path('rawsql', get_posts_by_query),
]
