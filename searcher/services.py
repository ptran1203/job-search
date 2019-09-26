from post.models import Post
from helper import common as commonHelper
from .models import Searcher, Keywords, Vocabulary, VectorSpace
from django.db.models import Q


def search_result(query):
    terms = commonHelper.cleaned_text(commonHelper.norm_text(query))
    dj_query = get_query(terms)
    posts = Post.objects.filter(dj_query)

    vocab = Vocabulary.objects.all()[0].get()
    searcher = Searcher(posts, vocab)

    doc_ids = searcher.search(terms)
    posts = Post.objects.filter(pk__in=doc_ids)

    upsert_keywords(terms)
    # nothing found mark keywords not in collection
    # if len(posts) == 0:
    #     upsert_keywords(terms, 0)

    return get_results(posts, doc_ids, terms)
    

def get_results(docs, ids, terms):
    """
    get docs by ids
    """
    doc_map = {}
    for doc in docs:
        doc_obj = doc.json_object()
        doc_obj['title'] = doc.title
        doc_obj['content'] = doc.content
        doc_obj['title_m'] = commonHelper.color_matches(terms, doc.title)
        doc_obj['content_m'] = commonHelper.color_matches_long(terms,
                doc.content)
        doc_map[doc.id] = doc_obj
    return [doc_map[id] for id in ids]


def upsert_keywords(terms):
    for term in terms:
        keyword, created = Keywords.objects.get_or_create(
            word=term
        )
        # this is new keyword
        if not created:
            keyword.num_of_searches += 1
            keyword.save()


def get_query(terms):
    if not terms:
        return

    is_contain = lambda term: Q(title__icontains=term) | \
                        Q(content__icontains=term) | \
                        Q(salary_range__icontains=term)

    condition = is_contain(terms[0])
    for term in terms[1:]:
        condition = condition | is_contain(term)
    return condition