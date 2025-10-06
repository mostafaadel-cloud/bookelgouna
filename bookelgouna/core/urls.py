from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^$', views.save_dates_and_explore, name='index'),
    url(r'^explore/$', TemplateView.as_view(template_name='core/explore.html'), name='explore'),
    url(r'^terms/$', TemplateView.as_view(template_name='core/terms.html'), name='terms'),
    url(r'^privacy_policy/$', TemplateView.as_view(template_name='core/privacy_policy.html'), name='privacy_policy'),
    url(r'^weather/$', views.weather, name='weather')

    # url(r'^SOME_URL_TO_USE_WITH$', TemplateView.as_view(template_name='core/YOUR_NEW_FILE.html'))
)
