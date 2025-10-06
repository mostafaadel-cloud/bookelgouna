from braces.views import SuperuserRequiredMixin
from django.db.models import Prefetch
from haystack.views import SearchView
from skd_tools.mixins import ActiveTabMixin

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import DetailView, ListView, View
from django.utils.translation import ugettext_lazy as _

from common.mixins import AjaxNewCommentMixin, CommentList
from users.mixins import EndUserOnlyMixin

from .forms import BlogCommentForm, BlogPostSearchForm
from .mixins import CategoriesToContextMixin, BlogPaginationMixin
from .models import BlogPost, BlogComment, Category


class BlogView(CategoriesToContextMixin, BlogPaginationMixin, ActiveTabMixin, ListView):
    active_tab = 'blog'
    template_name = "blog/blog.html"
    paginate_by = 5
    context_object_name = "posts"
    base_blog_url = reverse_lazy('blog')
    is_filtered_by_category = False

    def get_queryset(self):
        return BlogPost.objects.prefetch_related("category__translations", "translations").prefetch_related(
            Prefetch("comments", queryset=BlogComment.displayable.all()))

    def get_base_blog_url(self):
        return self.base_blog_url

    def get_is_filtered_by_category(self):
        return self.is_filtered_by_category

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['pages'] = self.structure_pages(context['page_obj'], context['paginator'])
        context['BASE_BLOG_URL'] = self.get_base_blog_url()
        context['FILTERED_BY_CATEGORY'] = self.get_is_filtered_by_category()
        return context


blog = BlogView.as_view()


class BlogCategoryView(BlogView):
    is_filtered_by_category = True

    def get_queryset(self):
        category = get_object_or_404(Category, slug__iexact=self.kwargs['slug'])
        return category.posts.prefetch_related("translations").prefetch_related(
            Prefetch("comments", queryset=BlogComment.displayable.all()))

    def get_base_blog_url(self):
        return reverse('blog_category', kwargs={'slug': self.kwargs['slug']})

blog_category = BlogCategoryView.as_view()


class BlogSearchView(BlogPaginationMixin, SearchView):
    active_tab = 'blog'
    template = "blog/search.html"
    base_blog_url = reverse_lazy('blog_search')
    is_filtered_by_category = False

    def __init__(self, *args, **kwargs):
        kwargs['form_class'] = BlogPostSearchForm
        super(BlogSearchView, self).__init__(*args, **kwargs)

    def get_base_blog_url(self):
        return self.base_blog_url

    def get_is_filtered_by_category(self):
        return self.is_filtered_by_category

    def get_results(self):
        return super(BlogSearchView, self).get_results().order_by('-id')

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page_obj) = self.build_page()
        is_paginated = page_obj.has_other_pages()

        context = {
            'active_tab': self.active_tab,
            'query': self.query,
            'form': self.form,
            'suggestion': None,
            'paginator': paginator,
            'page_obj': page_obj,
            'is_paginated': is_paginated,
            'categories': Category.objects.all(),
            'pages': self.structure_pages(page_obj, paginator),
            'BASE_BLOG_URL': self.get_base_blog_url(),
            'FILTERED_BY_CATEGORY': self.get_is_filtered_by_category()
        }

        if self.query:
            context['PAGINATION_URL_PARAMS'] = u"&amp;q={}".format(self.query)

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))


search = BlogSearchView()


class PostView(CategoriesToContextMixin, ActiveTabMixin, DetailView):
    active_tab = 'blog'
    template_name = "blog/post.html"
    model = BlogPost
    context_object_name = "post"
    base_blog_url = reverse_lazy('blog')
    comments_paginated_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        comments = BlogComment.displayable.filter(entity_id=self.object.pk).select_related("creator")
        context['comments_count'] = comments.count()
        context['has_more_comments'] = context['comments_count'] > self.comments_paginated_by
        context['comments'] = comments[:self.comments_paginated_by]
        context['can_add_comment'] = False
        user = self.request.user
        if user.is_authenticated() and user.is_end_user() and not user.is_staff:
            context['can_add_comment'] = not self.request.user.post_comments.filter(entity_id=self.object.pk).exists()
        elif not user.is_authenticated():
            context['can_add_comment'] = True
            context['login_url'] = '{}?next={}?scroll=1'.format(reverse('account_login'), self.request.path)
        if context['can_add_comment']:
            initial_comment_form = {
                'entity_id': self.object.pk,
            }
            context['comment_form'] = BlogCommentForm(prefix='comment', initial=initial_comment_form)
        if 'HTTP_REFERER' in self.request.META:
            back_url = self.request.META['HTTP_REFERER']
        else:
            back_url = reverse_lazy('blog')
        context['back_url'] = back_url
        return context


post = PostView.as_view()


class NewBlogCommentView(EndUserOnlyMixin, AjaxNewCommentMixin, View):
    ajax_template_name = "blog/includes/ajax_comment_form_block.html"
    form_class = BlogCommentForm
    model = BlogComment

new_blog_comment = NewBlogCommentView.as_view()


class BlogCommentList(CommentList, View):
    ajax_template_name = "blog/comment_list.html"
    model = BlogComment
    paginated_by = 20


comment_list = BlogCommentList.as_view()


class RebuildIndexesView(SuperuserRequiredMixin, View):
    def async_index_rebuild(self):
        from multiprocessing import Process
        p = Process(target=call_command, args=("rebuild_solr_indexes",))
        from django.db import connection
        connection.close()
        p.start()

    def get(self, request, *args, **kwargs):
        self.async_index_rebuild()
        messages.success(request, _('Search indexes were successfully updated.'))
        return HttpResponseRedirect(reverse('admin:index'))

rebuild_indexes = RebuildIndexesView.as_view()
