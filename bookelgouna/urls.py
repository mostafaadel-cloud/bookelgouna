from django.conf.urls.i18n import i18n_patterns
from rosetta.access import can_translate
from rosetta.views import home, list_languages, download_file, lang_sel, translate_text

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()


urlpatterns = i18n_patterns('',
    url(r'^', include('core.urls')),
    url(r'^', include('hotels.urls')),
    url(r'^', include('apartments.urls')),
    url(r'^', include('excursions.urls')),
    url(r'^', include('sports.urls')),
    url(r'^', include('transport.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('booking.urls')),
    url(r'^', include('entertainment.urls')),

    url(r'^blog/', include('blog.urls')),

    url(r'^business/', include('common.urls')),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^ckeditor/', include('ckeditor.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    url(r'^i18n/setlang/$', 'common.i18n_views.set_language', name='set_language'),
)


if settings.ENABLE_ROSETTA and 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += i18n_patterns('',
        url(r'^rosetta/$', user_passes_test(lambda u: can_translate(u), settings.ADMIN_LOGIN_URL)(home), name='rosetta-home'),
        url(r'^rosetta/pick/$', user_passes_test(lambda u: can_translate(u), settings.ADMIN_LOGIN_URL)(list_languages), name='rosetta-pick-file'),
        url(r'^rosetta/download/$', user_passes_test(lambda u: can_translate(u), settings.ADMIN_LOGIN_URL)(download_file), name='rosetta-download-file'),
        url(r'^rosetta/select/(?P<langid>[\w\-_\.]+)/(?P<idx>\d+)/$', user_passes_test(lambda u: can_translate(u), settings.ADMIN_LOGIN_URL)(lang_sel), name='rosetta-language-selection'),
        url(r'^rosetta/translate/$', user_passes_test(lambda u: can_translate(u), settings.ADMIN_LOGIN_URL)(translate_text), name='translate_text'),
    )

urlpatterns += i18n_patterns('',
    url(r'^', include('flatpages_i18n.urls')),
)
