from scipy import spatial
import unidecode
import re
import constant 

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
    accept = lambda x: x not in constant.STOPWORDS and not x.isdigit()
    return [word for word in words if accept(word)]

def cleaned_text(text):
    return remove_stopword(
        split(norm_text(text))
    )

def mark_content(terms, text):
    """
    color matches text and query
    """
    final = ''
    for term in terms:
        term_regex = r'\W{}\W'.format(term)
        match = re.search(term_regex, text, re.IGNORECASE)
        if match:
            start, end = match.span()
            matching = match.group(0)
            final += text.replace(
                matching,
                color_style(matching)
                )[safe_index(start) : end + 150]
    return get_final(final) or text[:250] + "..."

def get_final(final_res):
    if final_res == '':
        return None
    return ".." + " ".join(final_res.split(" ")[1: len(final_res) - 1]) + "...<br>"

def mark_title(terms, text):
    """
    color matches text and query
    """
    for term in terms:
        term_regex = r'\W{}\W'.format(term)
        match = re.search(term_regex, text, re.IGNORECASE)
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
    if index <= 150:
        return 0
    return index - 150