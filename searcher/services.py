from post.models import Post
from helper import processor
from .models import Searcher, Keywords, Vocabulary
from django.db.models import Q
from django.contrib.humanize.templatetags import humanize


def search_result(query):
    terms = processor.cleaned_text(processor.norm_text(query))
    dj_query = get_query(terms)
    posts = Post.objects.filter(dj_query)

    vocab = Vocabulary.objects.all()[0].get()
    searcher = Searcher(posts, vocab)

    doc_ids = searcher.search(terms)
    posts = Post.objects.filter(pk__in=doc_ids)

    upsert_keywords(query)
    return get_results(posts, doc_ids, terms)


def get_results(docs, ids, terms):
    """
    get docs by ids
    """
    doc_map = {}
    for doc in docs:
        doc_obj = doc.json_object(['title', 'content'])
        doc_obj['post_date'] = humanize.naturaltime(doc_obj['post_date'])
        doc_obj['title_m'] = processor.mark_title(terms, doc.title)
        doc_obj['content_m'] = processor.mark_content(terms,
                                                    doc.content)

        doc_map[doc.id] = doc_obj
    return [doc_map[id] for id in ids]


def upsert_keywords(word):
    keyword, created = Keywords.objects.get_or_create(
        word=word
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