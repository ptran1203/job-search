from scipy import spatial
import unidecode

def cosine(v1, v2):
    return 1 - spatial.distance.cosine(v1, v2)

def norm_text(text):
    return unidecode.unidecode(text.lower())