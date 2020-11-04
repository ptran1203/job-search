from django.shortcuts import render
from .models import Post
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from helper import slack
from django.utils import timezone
from django.db import connection
from django.contrib.humanize.templatetags import humanize
import json
import datetime
from helper import pagination
from constant import API_KEY
from salary_estimation.salary_prediction import salary_estimator

sort_types = {
    1: "-post_date",
    2: "post_date",
    3: "-salary_range",
    4: "salary_range",
    5: "-id",
    6: "id",
}


@csrf_exempt
def store_post(request):
    """
    Handle post request from crawler
    """
    if request.method != "POST":
        return HttpResponse("please correct your request")

    data = json.loads(request.body.decode("utf8"))
    Post.create(data)
    return HttpResponse("Ok")


def detail(request, id):
    """
    Get data for specific post
    """
    fields = (request.GET.get("fields") or "").split(",")
    if fields:
        try:
            return JsonResponse(Post.objects.values(*fields).get(pk=id))
        except:
            pass
    post = Post.objects.get(pk=id)
    return JsonResponse(post.json_object())


def count(request):
    """
    Count item in DB
    """
    return JsonResponse({"count": Post.objects.count()})


def clean(request):
    """
    delete out of date post
    """
    date_15daysago = timezone.now() - datetime.timedelta(days=45)
    count = Post.objects.filter(post_date__lt=date_15daysago).count()
    Post.objects.filter(post_date__lt=date_15daysago).delete()
    slack.send("deleted %s posts" % (count))
    return JsonResponse({"deleted": count})


def get_posts(request):
    query = request.GET
    limit = query.get("limit", 30)
    sort = int(query.get("sort", 1))
    page = int(query.get("page", 1))
    condition = query.get("condition", "")
    if sort in sort_types:
        sort = sort_types[sort]
    else:
        sort = 1

    return JsonResponse(pagination.sub(_posts(sort), page), safe=False)


def get_posts_by_query(request):
    # validation
    if request.GET.get("api_key", "") != API_KEY:
        return JsonResponse({"msg": "bad request"})

    sql = "SELECT *" "FROM post_post LIMIT 20;"

    if request.method == "POST":
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        sql = body["sql"]
    if request.method == "GET":
        sql = request.GET.get("sql")

    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        posts = cursor.fetchall()
        return JsonResponse(posts, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)})


def estimate_salary(request, id):
    post = Post.objects.get(pk=id)
    return JsonResponse({"salary": post.estimate_salary()})


def estimate_salary_text(request):
    text = request.body.decode("utf-8")
    return JsonResponse({"salary": salary_estimator.predict_from_text(text)})


# --                 utils                -- #
def _posts(sort):
    posts = [post.json_object() for post in Post.objects.all().order_by(sort)[:200]]

    # truncate content
    for post in posts:
        post["content_m"] = post["content"][:255] + "..."
        post["title_m"] = post["title"]
        post["post_date"] = humanize.naturaltime(post["post_date"])
        post.pop("content", None)
        post.pop("title", None)
    return posts
