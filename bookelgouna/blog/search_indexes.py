from haystack import indexes

from .models import BlogPost


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.SearchField(document=True, use_template=True)

    def get_model(self):
        return BlogPost

    def index_queryset(self, using=None):
        return BlogPost.objects.language(using).all()
