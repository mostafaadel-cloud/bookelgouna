from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns('',
    url(r'^create_service/$', views.create_service, name='create_service'),
    url(r'^update_service/',
        include(patterns('',
                         url(r'^$', views.update_service, name='update_service'),
                         url(r'^(?P<slug>[A-Za-z0-9_\-]+)/$', views.update_service, name='update_service_with_slug')))),
    url(r'^not_implemented/$', views.not_implemented, name='not_implemented'),
    url(r'^create_item/$', views.create_item, name='create_item'),
    url(r'^update_item/(?P<slug>[A-Za-z0-9_\-]+)/$', views.update_item, name='update_item'),
    url(r'^items_list/$', views.items_list, name='items_list'),

    url(r'^save_date_ajax/$', views.save_dates_and_guests_ajax, name='save_dates_ajax'),
    url(r'^save_dates_and_explore/$', views.save_dates_and_explore, name='save_dates_and_explore')
)

urlpatterns += patterns('common.views',
                        url(r'^upload_featured_image/$', 'upload_featured_image', name='upload_featured_image'),
                        url(r'^upload_gallery_images/$', 'upload_gallery_images', name='upload_gallery_images'),
                        url(r'^delete_temp_image/$', 'delete_temp_image', name='delete_temp_image'))
