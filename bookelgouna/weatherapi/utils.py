import requests

from django.utils.translation import get_language
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings


lang2wulang = {
    'en': 'EN',
    'ar': 'AR',
    'de': 'DL',  # it differs
    'ru': 'RU',
    'it': 'IT',
    'fr': 'FR'
}


def get_current_weather_info():
    loc = settings.WUNDERGROUND_LOCATION
    lang = get_language()
    cache_key = "wunderground_%s_%s" % (loc, lang)
    weather_info = cache.get(cache_key)
    if not weather_info:
        root_url = settings.WUNDERGROUND_ROOT_URL
        key = settings.WUNDERGROUND_API_KEY
        url = root_url + '%s/conditions/lang:%s/q/%s.json' % (key, lang2wulang[lang], loc)
        resp = requests.get(url)
        if resp.status_code == 200:
            weather_info = resp.json()
            now = timezone.now()
            mins = 60 - now.minute
            cache.set(cache_key, weather_info, mins * 60)  # should expire on the beginning of next hour
        else:
            weather_info = {}
    return weather_info
