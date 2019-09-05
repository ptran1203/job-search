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
    doc_ids = searcher.search(query)
    docs = Post.objects.filter(pk__in=doc_ids)
    return HttpResponse(
        serializers.serialize('json', sort_docs(docs, doc_ids)),
        content_type="application/json")

## helper

def sort_docs(docs, ids):
    """
    sort docs by ids
    """
    doc_map = {doc.id: doc for doc in docs}
    for doc in docs:
        doc.title = color_matches(query, doc.title.lower())
        doc.content = color_matches(query, doc.content.lower())
        doc_map[doc.id] = doc
    return [doc_map[id] for id in ids]

def color_matches(query, text):
    query = query.lower()
    return text.replace(query, color_style(query))

def color_style(word):
    return '<span style="color:green">' + word + '</span>'
