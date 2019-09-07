from django.shortcuts import render
from post.models import Post
from django.http import (
    HttpResponseRedirect, Http404,
    JsonResponse, HttpResponse
)
from django.views.decorators.csrf import csrf_exempt
from .models import Searcher
from .vector_space import Vocabulary
from django.core import serializers
from helper import common as commonHelper

def buildVS(request):
    from .vector_space import VectorSpace
    V = VectorSpace()
    return JsonResponse({
        "status": "Done",
        "size": V.size
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
    print(terms)
    docs = Post.objects.filter(pk__in=doc_ids)
    return HttpResponse(
        serializers.serialize(
            'json',
            get_results(docs, doc_ids, terms)),
            content_type="application/json")

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
