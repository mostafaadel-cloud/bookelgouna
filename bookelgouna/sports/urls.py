from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^find_sport/$', views.find_sport, name='find_sport'),
    url(r'^view_sport/(?P<slug>[A-Za-z0-9_\-]+)/$', views.view_sport, name='view_sport'),
    url(r'^add_sport_items_to_cart/$', views.add_items_to_cart, name='add_sport_items_to_cart'),
    url(r'^sport/new_comment/$', views.new_sport_comment, name='new_sportcomment'),
    url(r'^sport/comment_list/$', views.comment_list, name='sport_comment_list'),
    url(r'^sport/new_review/$', views.new_sport_review, name='new_sport_review'),
    url(r'^business/sport_gallery_image_crop/(?P<pk>\d+)/$', views.sport_gallery_image_crop,
        name='sport_gallery_image_crop'),
    url(r'^business/sport_featured_image_crop/(?P<pk>\d+)/$', views.sport_featured_image_crop,
        name='sport_featured_image_crop'),
    url(r'^business/sport_item_featured_image_crop/(?P<pk>\d+)/$', views.sport_item_image_crop,
        name='sport_item_featured_image_crop'),
    url(r'^business/sport_item_gallery_image_crop/(?P<pk>\d+)/$', views.sport_item_gallery_image_crop,
        name='sport_item_gallery_image_crop'),
    url(r'^business/remove_sport_item/(?P<slug>[A-Za-z0-9_\-]+)/$', views.remove_item,
        name='remove_sport_item'),
    url(r'^business/sport_item/(?P<slug>[A-Za-z0-9_\-]+)/show_on_site/$', views.item_show_on_site_attr_change,
        name='sport_item_show_on_site_attr_change'),
    url(r'^business/sport_item/(?P<slug>[A-Za-z0-9_\-]+)/number/$', views.item_number_attr_change,
        name='sport_item_number_attr_change'),
)
