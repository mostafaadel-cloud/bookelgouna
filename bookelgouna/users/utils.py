from django_countries import countries
import os
from ipware.ip import get_real_ip

from django.contrib.gis.geoip import GeoIP
from django.conf import settings


def get_country_code_by_ip_using_geoip(request, return_default=True):
    """
    :param request:
    :return: country code calculated by request meta data using geoip lib. if country code cannot be defined or
    is invalid and return_default setting is True then default country is returned otherwise None
    """

    ip = get_real_ip(request)
    if ip is not None:
        gi = GeoIP(path=os.path.join(settings.STATIC_ROOT, 'GeoIP.dat'))
        country_code = gi.country_code(ip)
        if country_code in countries:
            return country_code
    return 'EG' if return_default else None
