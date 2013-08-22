from haystack import indexes
from aliases.models import Alias

class AliasIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Alias

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.get_active()
