from django.shortcuts import render
from post.models import Post
from django.http import (
    HttpResponseRedirect, Http404,
    JsonResponse, HttpResponse
)
from django.views.decorators.csrf import csrf_exempt
from .models import Searcher
from .vector_space import Vocabulary


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
    res = searcher.search(query)
    print(res)
    return HttpResponse("ok")