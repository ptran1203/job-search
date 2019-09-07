from django.contrib import admin
from .vector_space import Vocabulary
from .models import Keywords
# Register your models here.
admin.site.register(Vocabulary)
admin.site.register(Keywords)