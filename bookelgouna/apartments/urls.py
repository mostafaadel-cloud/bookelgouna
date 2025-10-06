from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^find_apartment/$', views.find_apartment, name='find_apartment'),
    url(r'^view_apartment/(?P<slug>[A-Za-z0-9_\-]+)/$', views.view_apartment, name='view_apartment'),
    url(r'^add_apartment_to_cart/$', views.add_apartment_to_cart, name='add_apartment_to_cart'),
    url(r'^business/apt_gallery_image_crop/(?P<pk>\d+)/$', views.apt_gallery_image_crop,
        name='apt_gallery_image_crop'),
    url(r'^business/apt_featured_image_crop/(?P<pk>\d+)/$', views.apt_featured_image_crop,
        name='apt_featured_image_crop'),
    # url(r'^business/remove_apt/(?P<slug>[A-Za-z0-9_\-]+)/$', views.remove_apt, name='remove_apt'),
    url(r'^business/apt/(?P<slug>[A-Za-z0-9_\-]+)/show_on_site/$', views.apt_show_on_site_attr_change,
        name='apt_show_on_site_attr_change'),
    url(r'^business/apt_prices/list/(?P<slug>[A-Za-z0-9_\-]+)/$', views.apt_prices, name='apt_prices'),
    url(r'^business/apt_opts/(?P<slug>[A-Za-z0-9_\-]+)/$', views.apt_options_view, name='apt_options'),
    url(r'^business/apt_prices/new/(?P<slug>[A-Za-z0-9_\-]+)/$', views.apt_price_category_create,
        name='apt_price_category_create'),
    url(r'^business/apt_prices/edit/(?P<pk>\d+)/$', views.apt_price_category_update,
        name='apt_price_category_update'),
    url(r'^business/apt_prices/view/(?P<pk>\d+)/$', views.apt_price_category_view,
        name='apt_price_category_view'),
    url(r'^business/apt_prices/delete/(?P<pk>\d+)/$', views.apt_price_category_delete,
        name='apt_price_category_delete'),
    url(r'^business/apt_prices/delete_special_price/(?P<pk>\d+)/$', views.apt_special_price_delete,
        name='apt_special_price_delete'),
    url(r'^apartment/new_comment/$', views.new_apartment_comment, name='new_apartmentcomment'),
    url(r'^apartment/comment_list/$', views.comment_list, name='apartment_comment_list'),
    url(r'^apartment/new_review/$', views.new_apartment_review, name='new_apartment_review')
)
