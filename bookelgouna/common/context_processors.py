from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.utils import timezone

from .models import Language
from .forms import DatesAndGuestsAjaxForm
from .utils import get_absolute_url


def robots_directives(request):
    if settings.ALLOW_ROBOTS:
        return {'ROBOTS_DIRECTIVES': 'INDEX,FOLLOW'}
    else:
        return {'ROBOTS_DIRECTIVES': 'NOINDEX,NOFOLLOW'}


def google_analytics(request):
    return {'USE_GOOGLE_ANALYTICS': settings.USE_GOOGLE_ANALYTICS}


def default_fb_image(request):
    default_url = settings.DEFAULT_FB_IMAGE
    if default_url.startswith(settings.STATIC_URL):
        raise ImproperlyConfigured(
            'Default facebook image should not start from static url prefix. It\'s prepending automatically.')
    else:
        default_url = static(default_url)
    return {'DEFAULT_FB_IMAGE': get_absolute_url(request, default_url)}


def travel_dates(request):
    initial = {}
    required_keys = ['arrival', 'departure', 'adults', 'children']
    if all([key in request.session for key in required_keys]):
        today = timezone.now().date()
        if request.session['arrival'] >= today:
            initial = {key: request.session[key] for key in required_keys}
        else:
            for key in required_keys:
                del request.session[key]
    form = DatesAndGuestsAjaxForm(initial=initial)
    return {'dates_and_guests_form': form}


def enabled_languages(request):
    all_languages = settings.LANGUAGES
    enabled_langs = []
    disabled_languages = Language.objects.filter(is_enabled=False)
    if disabled_languages.exists() > 0:
        disabled_languages = disabled_languages.values('code')
        for code, name in all_languages:
            disable = False
            for disabled_language in disabled_languages:
                if code == disabled_language['code']:
                    disable = True
                    break
            if not disable:
                enabled_langs.append((code, name))
        return {'ENABLED_LANGUAGES': enabled_langs}
    else:
        return {'ENABLED_LANGUAGES': all_languages}
