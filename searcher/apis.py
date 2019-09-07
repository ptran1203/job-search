from django.shortcuts import render
from post.models import Post
from django.http import (
    HttpResponseRedirect, Http404,
    JsonResponse, HttpResponse
)
from django.views.decorators.csrf import csrf_exempt
from .models import Searcher, Keywords
from .vector_space import Vocabulary, VectorSpace
from django.core import serializers
from helper import common as commonHelper
from helper import http as httpHelper

def buildVS(request):
    try:
        V = VectorSpace()
        return JsonResponse({
            "status": "Done",
            "size": V.size
            })
    except:
        return JsonResponse({
            "status": "Error!",
            "size": 0
            })


def search(request):
    docs = Post.objects.all()
    vocab = Vocabulary.objects.all()[0].get()
    searcher = Searcher(docs, vocab)
    query = request.GET.get('q')

    if not query:
        return HttpResponse("no query")

    terms = commonHelper.cleaned_text(commonHelper.norm_text(query))

    doc_ids = searcher.search(terms)
    docs = Post.objects.filter(pk__in=doc_ids)

    upsert_keywords(terms)
    # nothing found mark keywords not in collection
    # if len(docs) == 0:
    #     upsert_keywords(terms, 0)

    return httpHelper.json_response(
        get_results(docs, doc_ids, terms)
    )

def keywords(request):
    return httpHelper.json_response(
        Keywords.objects.all()
    )

## helper

def get_results(docs, ids, terms):
    """
    get docs by ids
    """
    doc_map = {doc.id: doc for doc in docs}
    for doc in docs:
        doc.title = commonHelper.color_matches(terms, doc.title)
        doc.content = commonHelper.color_matches_long(terms, doc.content)
        doc_map[doc.id] = doc
    return [doc_map[id] for id in ids]

def upsert_keywords(terms):
    for term in terms:
        keyword, created = Keywords.objects.get_or_create(
            word=term
        )

        # print(keyword, created)
        # this is new keyword
        if not created:
            keyword.num_of_searches += 1
            keyword.save()
