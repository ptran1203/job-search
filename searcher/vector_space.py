from post.models import Post
import re
import unidecode # remove accents

# build vector space model
class VectorSpace:
    def __init__(self):
        """
        Create vsmodel
        """
        vocab, posts = self.init_vocab_posts()
        self.size = self.build(vocab, posts)
    
    def __str__(self):
        return self.size

    def init_vocab_posts(self):
        """
        Initialize vocabulaty from posts
        """
        posts = Post.objects.all()
        vocab = set()
        for post in posts:
            [vocab.add(_) for _ in \
                self._split(self._norm(post.get_text()))]

        return list(vocab), posts

    @staticmethod
    def _split(text):
        """
        split string into characters
        """
        return [ _ for _ in re.split(
            r'[^\w]',
            text.strip()) 
            if _ != '']

    @staticmethod
    def _norm(text):
        return unidecode.unidecode(text.lower())

    def build(self, vocab, posts):
        """
        Start build vector for each post
        return number of posts
        """
        post_map = {p.id:[0]*len(vocab) for p in posts}
        for post in posts:
            for word in self._split(self._norm(post.get_text())):
                try:
                    post_map[post.id][vocab.index(word)] += 1
                except KeyError:
                    print("WARNING: ", post.id, "not in map")

        for post in posts:
            post.set_vector(post_map[post.id])
        return len(post_map)
