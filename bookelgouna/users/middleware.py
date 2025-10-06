# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import is_valid_path
from django.middleware.locale import LocaleMiddleware
from django.utils.cache import patch_vary_headers
from django.utils import translation

from common.models import is_enabled_language

from .models import Country
from .utils import get_country_code_by_ip_using_geoip


class LocaleDetectionMiddleware(LocaleMiddleware):
    """
    Except functionality provided by LocaleMiddleware it processes this situation:
    If user accesses url without language prefix, i.e. /find_hotel/ this middleware tries to get correct language
    in two additional ways:
    1. if user is authenticated it takes user preferred_language field
    2. if user is anonymous then it tries to detect country by ip and get that country default_language field. If
    country cannot be determinated then it uses django.utils.translation.get_language() method.
    """
    def process_response(self, request, response):
        language = translation.get_language()
        language_from_path = translation.get_language_from_path(request.path_info)
        language_changed = False
        if (response.status_code == 404 and not language_from_path
                and self.is_language_prefix_patterns_used()):
            # CHANGED PART START
            if hasattr(request, 'user'):
                if request.user.is_authenticated():
                    preferred_language_by_user = request.user.preferred_language
                    if is_enabled_language(preferred_language_by_user):
                        language = preferred_language_by_user
                        language_changed = True
                else:
                    country_code = get_country_code_by_ip_using_geoip(request, return_default=False)
                    if country_code:
                        try:
                            country = Country.objects.get(name=country_code)
                        except Country.DoesNotExist:
                            pass
                        else:
                            default_country_language = country.default_language
                            if is_enabled_language(default_country_language):
                                language = default_country_language
                                language_changed = True
            else:
                raise ImproperlyConfigured('LocaleDetectionMiddleware should be listed in MIDDLEWARE_CLASSES after '
                                           '"django.contrib.auth.middleware.AuthenticationMiddleware".')
            if language_changed:
                translation.activate(language)
            # CHANGED PART END
            urlconf = getattr(request, 'urlconf', None)
            language_path = '/%s%s' % (language, request.path_info)
            path_valid = is_valid_path(language_path, urlconf)
            if (not path_valid and settings.APPEND_SLASH
                    and not language_path.endswith('/')):
                path_valid = is_valid_path("%s/" % language_path, urlconf)

            if path_valid:
                language_url = "%s://%s/%s%s" % (
                    request.scheme, request.get_host(), language,
                    request.get_full_path())
                return self.response_redirect_class(language_url)

        if not (self.is_language_prefix_patterns_used()
                and language_from_path):
            patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response
