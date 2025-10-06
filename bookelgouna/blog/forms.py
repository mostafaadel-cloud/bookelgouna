from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

from django import forms
from django.utils.translation import ugettext_lazy as _, get_language

from .models import BlogComment, BlogPost


class BlogCommentForm(forms.ModelForm):
    entity_id = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BlogCommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BlogComment
        fields = ('text',)

    def clean(self):
        entity_id = self.cleaned_data.get('entity_id')
        if entity_id:
            user = self.request.user
            if user.is_authenticated() and user.is_end_user():
                try:
                    BlogPost.objects.get(pk=entity_id)
                except BlogPost.DoesNotExist:
                    raise forms.ValidationError(_('No blog post with this pk.'))
                if user.post_comments.filter(entity_id=entity_id).exists():
                    raise forms.ValidationError(_('You have added comment earlier. It might not have been approved yet.'))
            else:
                raise forms.ValidationError(_('Only authorized clients can add new comments.'))


class BlogPostSearchForm(ModelSearchForm):
    def __init__(self, *args, **kwargs):
        kwargs['searchqueryset'] = SearchQuerySet().using(get_language())
        super(BlogPostSearchForm, self).__init__(*args, **kwargs)
