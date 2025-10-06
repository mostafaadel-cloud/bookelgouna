from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^find_hotel/$', views.find_hotel, name='find_hotel'),
    url(r'^view_hotel/(?P<slug>[A-Za-z0-9_\-]+)/$', views.view_hotel, name='view_hotel'),
    url(r'^add_rooms_to_cart/$', views.add_rooms_to_cart, name='add_rooms_to_cart'),
    url(r'^business/hotel_gallery_image_crop/(?P<pk>\d+)/$', views.hotel_gallery_image_crop,
        name='hotel_gallery_image_crop'),
    url(r'^business/hotel_featured_image_crop/(?P<pk>\d+)/$', views.hotel_featured_image_crop,
        name='hotel_featured_image_crop'),
    url(r'^business/room_image_crop/(?P<pk>\d+)/$', views.room_image_crop,
        name='room_image_crop'),
    url(r'^business/remove_room/(?P<slug>[A-Za-z0-9_\-]+)/$', views.remove_room, name='remove_room'),
    url(r'^business/room/(?P<slug>[A-Za-z0-9_\-]+)/show_on_site/$', views.room_show_on_site_attr_change,
        name='room_show_on_site_attr_change'),
    url(r'^business/room/(?P<slug>[A-Za-z0-9_\-]+)/allotment/$', views.room_allotment_attr_change,
        name='room_allotment_attr_change'),
    url(r'^business/room_prices/list/(?P<slug>[A-Za-z0-9_\-]+)/$', views.room_prices, name='room_prices'),
    url(r'^business/room_prices/new/(?P<slug>[A-Za-z0-9_\-]+)/$', views.room_price_category_create,
        name='room_price_category_create'),
    url(r'^business/room_prices/edit/(?P<pk>\d+)/$', views.room_price_category_update,
        name='room_price_category_update'),
    url(r'^business/room_prices/view/(?P<pk>\d+)/$', views.room_price_category_view,
        name='room_price_category_view'),
    url(r'^business/room_prices/delete/(?P<pk>\d+)/$', views.room_price_category_delete,
        name='room_price_category_delete'),
    url(r'^business/room_prices/delete_special_price/(?P<pk>\d+)/$', views.room_special_price_delete,
        name='room_special_price_delete'),
    url(r'^hotel/new_comment/$', views.new_hotel_comment, name='new_hotelcomment'),
    url(r'^hotel/comment_list/$', views.comment_list, name='hotel_comment_list'),
    url(r'^hotel/new_review/$', views.new_hotel_review, name='new_hotel_review')
)
