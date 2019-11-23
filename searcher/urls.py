from django.urls import path, re_path
from .apis import (
    buildVS,
    search,
    keywords
)

app_name = "searcher"

urlpatterns = [
    path('vectorspace', buildVS),
    path('search', search),
    path('keywords', keywords)
]