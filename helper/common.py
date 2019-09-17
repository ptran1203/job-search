from scipy import spatial
import unidecode
import re
from constant import common as commonConst 

def cosine(v1, v2):
    return 1 - spatial.distance.cosine(v1, v2)

def norm_text(text):
    """
    Remove accents and convert to lower 
    """
    return unidecode.unidecode(text.lower())

def split(text):
    """
    split string into characters
    """
    return [ _ for _ in re.split(
        r'[^\w]',
        text.strip()) 
        if _ != '']

def remove_stopword(words):
    """
    remove en, vi stopwords in words
    params: <list>
    return: <list>
    """
    accept = lambda x: x not in commonConst.STOPWORDS and not x.isdigit()
    return [word for word in words if accept(word)]

def cleaned_text(text):
    return remove_stopword(
        split(norm_text(text))
    )

def color_matches_long(terms, text):
    """
    color matches text and query
    """
    final = ''
    for term in terms:
        match = re.search(term, text, re.IGNORECASE)
        if match:
            start, end = match.span()
            matching = match.group(0)
            final += text.replace(
                matching,
                color_style(matching)
                )[safe_index(start) : end + 100]
    return final or text[:250]

def color_matches(terms, text):
    """
    color matches text and query
    """
    final = ''
    for term in terms:
        match = re.search(term, text, re.IGNORECASE)
        if match:
            matching = match.group(0)
            text = text.replace(
                matching,
                color_style(matching)
                )
    return text

def color_style(word):
    return '<span class="matched">' + word + '</span>'

def safe_index(index):
    if index <= 100:
        return 0
    return index - 100

def split_content(text):
    new_text = '<p>' + re.sub(
        r'[^\w+\s\,\:]', '</p><p> -',
        text) + '</p>'
    
    return new_text.replace('<p> -</p>', '')
