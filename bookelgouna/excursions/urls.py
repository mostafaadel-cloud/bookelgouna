from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^find_excursion/$', views.find_excursion, name='find_excursion'),
    url(r'^view_excursion/(?P<slug>[A-Za-z0-9_\-]+)/$', views.view_excursion, name='view_excursion'),
    url(r'^add_excursion_items_to_cart/$', views.add_items_to_cart, name='add_excursion_items_to_cart'),
    url(r'^excursion/new_comment/$', views.new_excursion_comment, name='new_excursioncomment'),
    url(r'^excursion/comment_list/$', views.comment_list, name='excursion_comment_list'),
    url(r'^excursion/new_review/$', views.new_excursion_review, name='new_excursion_review'),
    url(r'^business/excursion_gallery_image_crop/(?P<pk>\d+)/$', views.excursion_gallery_image_crop,
        name='excursion_gallery_image_crop'),
    url(r'^business/excursion_featured_image_crop/(?P<pk>\d+)/$', views.excursion_featured_image_crop,
        name='excursion_featured_image_crop'),
    url(r'^business/excursion_item_featured_image_crop/(?P<pk>\d+)/$', views.excursion_item_image_crop,
        name='excursion_item_featured_image_crop'),
    url(r'^business/excursion_item_gallery_image_crop/(?P<pk>\d+)/$', views.excursion_item_gallery_image_crop,
        name='excursion_item_gallery_image_crop'),
    url(r'^business/remove_excursion_item/(?P<slug>[A-Za-z0-9_\-]+)/$', views.remove_item,
        name='remove_excursion_item'),
    url(r'^business/excursion_item/(?P<slug>[A-Za-z0-9_\-]+)/show_on_site/$', views.item_show_on_site_attr_change,
        name='excursion_item_show_on_site_attr_change'),
    url(r'^business/excursion_item/(?P<slug>[A-Za-z0-9_\-]+)/number/$', views.item_number_attr_change,
        name='excursion_item_number_attr_change'),
)
