from datetime import date, datetime, timedelta
from django.core.urlresolvers import reverse
from django_countries import countries
import requests
import tempfile
from phonenumbers import country_code_for_valid_region

from django.core import files
from django.utils import timezone


def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


def get_now_if_date_is_today_or_noon_of_that_date(d):
    now = timezone.now()
    if d == now.date():
        result = now
    else:
        result = get_noon_of_this_date(d)
    return result


def get_noon_of_this_date(d):
    tz = timezone.get_current_timezone()
    result = tz.localize(datetime(d.year, d.month, d.day, 12, 0))
    return result


def default_arrival_date():
    """
    returns date to use as arrival by default if nothing was set by client
    """
    arrival = timezone.now().date() + timedelta(days=1)
    return arrival


def default_departure_date():
    """
    returns date to use as departure by default if nothing was set by client
    """
    departure = timezone.now().date() + timedelta(days=8)
    return departure


def get_arrival_from_session_or_default(request):
    return request.session.get('arrival', default_arrival_date())


def get_departure_from_session_or_default(request):
    return request.session.get('departure', default_departure_date())


def prepare_date(datetime_or_date):
    if isinstance(datetime_or_date, datetime):
        return datetime_or_date.date()
    else:
        return datetime_or_date


def get_absolute_url(request, relative_url):
    if relative_url is None or relative_url[:4] == 'http':
        return relative_url
    protocol = 'http'
    if request.is_secure():
        protocol = 'https'
    if relative_url[:2] == '//':
        return '%s:%s' % (protocol, relative_url)
    host = request.get_host()
    return '%s://%s%s' % (protocol, host, relative_url)


def download_file_from_url(url):
    # Stream the image from the url
    try:
        request = requests.get(url, stream=True)
    except requests.exceptions.RequestException as e:
        # TODO: log error here
        return None

    if request.status_code != requests.codes.ok:
        # TODO: log error here
        return None

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    return files.File(lf)


rare_country_codes = {
    'AQ': 672,
    'BV': 47,
    'GS': 500,
    # 'HM': '',
    # 'PN': '',
    # 'TF': '',
    # 'UM': ''
}


def is_valid_for_libphonenumber(country_geocode):
    try:
        country_code_for_valid_region(country_geocode)
    except Exception:
        return False
    else:
        return True


def get_phone_prefix_or_empty_string_for(country_geocode):
    try:
        country_phone_code = country_code_for_valid_region(country_geocode)
    except Exception:
        rare_code = rare_country_codes.get(country_geocode, '')
        if rare_code:
            rare_code = prepend_plus_prefix(rare_code)
        return rare_code
    else:
        return prepend_plus_prefix(country_phone_code)


def prepend_plus_prefix(country_phone_code):
    return u'+%d' % country_phone_code


def build_country2prefix_dict():
    country2prefix = {}
    for code, title in countries:
        country2prefix[code] = get_phone_prefix_or_empty_string_for(code)
    country2prefix[''] = ''  # empty country case
    return country2prefix


def get_admin_changelist_url(model_class):
    return reverse("admin:%s_%s_changelist" % (model_class._meta.app_label, model_class._meta.model_name))
