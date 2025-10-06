from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^cart/$', views.cart_view, name='cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^checkout2/$', views.checkout_enter_phone, name='checkout_enter_phone'),
    url(r'^change_orderitem/(?P<pk>\d+)/$', views.change_orderitem, name='change_orderitem'),
    url(r'^delete_cartitem/(?P<pk>\d+)/$', views.delete_cartitem, name='delete_cartitem'),
)
