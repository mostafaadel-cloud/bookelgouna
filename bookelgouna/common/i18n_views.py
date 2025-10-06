from urlparse import urlparse

from django import http
from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.utils import translation
from django.utils.http import is_safe_url
from django.utils.translation import check_for_language, LANGUAGE_SESSION_KEY


def set_language(request):
    """
    Redirect to a given url while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request. If called as a GET request, it will
    redirect to the page in the request (the 'next' parameter) without changing
    any state.
    """
    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    lang_code = request.POST.get('language', None)
    if request.method == 'POST':
        # We need to be able to filter out the language prefix from the next URL
        next = urlparse(next).path
        current_language = translation.get_language_from_path(next)
        translation.activate(current_language)
        next_data = resolve(next)
        translation.activate(lang_code)  # this should ensure we get the right URL for the next page
        next = reverse(next_data.view_name, args=next_data.args, kwargs=next_data.kwargs)
        response = http.HttpResponseRedirect(next)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                                    max_age=settings.LANGUAGE_COOKIE_AGE,
                                    path=settings.LANGUAGE_COOKIE_PATH,
                                    domain=settings.LANGUAGE_COOKIE_DOMAIN)
    else:
        response = http.HttpResponseRedirect(next)
    return response