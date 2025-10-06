from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^find_entertainment/$', views.find_entertainment, name='find_entertainment'),
    url(r'^view_entertainment/(?P<slug>[A-Za-z0-9_\-]+)/$', views.view_entertainment, name='view_entertainment'),
    url(r'^add_entertainment_items_to_cart/$', views.add_items_to_cart, name='add_entertainment_items_to_cart'),
    url(r'^entertainment/new_comment/$', views.new_entertainment_comment, name='new_entertainmentcomment'),
    url(r'^entertainment/comment_list/$', views.comment_list, name='entertainment_comment_list'),
    url(r'^entertainment/new_review/$', views.new_entertainment_review, name='new_entertainment_review'),
    url(r'^business/entertainment_gallery_image_crop/(?P<pk>\d+)/$', views.entertainment_gallery_image_crop,
        name='entertainment_gallery_image_crop'),
    url(r'^business/entertainment_featured_image_crop/(?P<pk>\d+)/$', views.entertainment_featured_image_crop,
        name='entertainment_featured_image_crop'),
    url(r'^business/entertainment_item_featured_image_crop/(?P<pk>\d+)/$', views.entertainment_item_image_crop,
        name='entertainment_item_featured_image_crop'),
    url(r'^business/entertainment_item_gallery_image_crop/(?P<pk>\d+)/$', views.entertainment_item_gallery_image_crop,
        name='entertainment_item_gallery_image_crop'),
    url(r'^business/remove_entertainment_item/(?P<slug>[A-Za-z0-9_\-]+)/$', views.remove_item,
        name='remove_entertainment_item'),
    url(r'^business/entertainment_item/(?P<slug>[A-Za-z0-9_\-]+)/show_on_site/$', views.item_show_on_site_attr_change,
        name='entertainment_item_show_on_site_attr_change'),
    url(r'^business/entertainment_item/(?P<slug>[A-Za-z0-9_\-]+)/number/$', views.item_number_attr_change,
        name='entertainment_item_number_attr_change'),
)
