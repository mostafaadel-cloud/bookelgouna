from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.blog, name='blog'),
    url(r'^search/', views.search, name='blog_search'),
    url(r'^new_comment/$', views.new_blog_comment, name='new_blogcomment'),
    url(r'^rebuild_indexes/$', views.rebuild_indexes, name='rebuild_solr_indexes'),
    url(r'^comment_list/$', views.comment_list, name='blog_comment_list'),
    url(r'^post/(?P<slug>[A-Za-z0-9_\-]+)/$', views.post, name='post'),
    url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$', views.blog_category, name='blog_category'),
)
