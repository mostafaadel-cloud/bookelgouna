from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^find_transport/$', views.find_transport, name='find_transport'),
    url(r'^view_transport/(?P<slug>[A-Za-z0-9_\-]+)/$', views.view_transport, name='view_transport'),
    url(r'^add_transport_items_to_cart/$', views.add_items_to_cart, name='add_transport_items_to_cart'),
    url(r'^business/transport_gallery_image_crop/(?P<pk>\d+)/$', views.transport_gallery_image_crop,
        name='transport_gallery_image_crop'),
    url(r'^business/transport_featured_image_crop/(?P<pk>\d+)/$', views.transport_featured_image_crop,
        name='transport_featured_image_crop'),
    url(r'^business/transport_item_featured_image_crop/(?P<pk>\d+)/$', views.transport_item_image_crop,
        name='transport_item_featured_image_crop'),
    url(r'^business/transport_item_gallery_image_crop/(?P<pk>\d+)/$', views.transport_item_gallery_image_crop,
        name='transport_item_gallery_image_crop'),
    url(r'^business/remove_transport_item/(?P<slug>[A-Za-z0-9_\-]+)/$', views.remove_item,
        name='remove_transport_item'),
    url(r'^business/transport_item/(?P<slug>[A-Za-z0-9_\-]+)/show_on_site/$', views.item_show_on_site_attr_change,
        name='transport_item_show_on_site_attr_change'),
    url(r'^business/transport_item/(?P<slug>[A-Za-z0-9_\-]+)/number/$', views.item_number_attr_change,
        name='transport_item_number_attr_change'),
    url(r'^transport/new_comment/$', views.new_transport_comment, name='new_transportcomment'),
    url(r'^transport/comment_list/$', views.comment_list, name='transport_comment_list'),
    url(r'^transport/new_review/$', views.new_transport_review, name='new_transport_review')
)
