from post.models import Post
from helper import common as commonHelper
from .models import Searcher, Keywords, Vocabulary, VectorSpace


def search_result(query):
    docs = Post.objects.all()
    vocab = Vocabulary.objects.all()[0].get()
    searcher = Searcher(docs, vocab)
    terms = commonHelper.cleaned_text(commonHelper.norm_text(query))
    doc_ids = searcher.search(terms)
    docs = Post.objects.filter(pk__in=doc_ids)

    upsert_keywords(terms)
    # nothing found mark keywords not in collection
    # if len(docs) == 0:
    #     upsert_keywords(terms, 0)

    return get_results(docs, doc_ids, terms)
    

def get_results(docs, ids, terms):
    """
    get docs by ids
    """
    doc_map = {}
    for doc in docs:
        doc_obj = doc.json_object(is_html=True)
        doc_obj['title'] = commonHelper.color_matches(terms, doc.title)
        doc_obj['content'] = commonHelper.color_matches_long(terms,
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
