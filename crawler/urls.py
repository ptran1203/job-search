from django.contrib import admin
from django.urls import path, re_path
from .apis import(
    crawl,
    )

app_name = "crawler"

urlpatterns = [
    path('crawl', crawl)
]


# import threading
# import requests

# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec)
#         func()
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     return t

# def ping():
# 	host_prod = "https://inomii.herokuapp.com"
# 	host_dev = "localhost:8000"
# 	r = requests.get(host_prod + '/api/crawler')
# 	print(r)

# # every 20 min -> 1200
# set_interval(ping, 1200)