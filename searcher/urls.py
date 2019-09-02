from django.urls import path, re_path
from .apis import (
    buildVS,
    search
)

app_name = "searcher"

urlpatterns = [
    path('vectorspace', buildVS),
    path('search', search)
]