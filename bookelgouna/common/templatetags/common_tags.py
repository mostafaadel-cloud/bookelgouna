# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from django.contrib.messages import constants
from django.templatetags.static import static
from widget_tweaks.templatetags.widget_tweaks import silence_without_field, add_class

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines

from hotels.models import Hotel, UnapprovedHotel, UnapprovedHotelComment, Room
from apartments.models import Apartment, UnapprovedApartment, UnapprovedApartmentComment
from transport.models import Transport, UnapprovedTransport, UnapprovedTransportComment
from sports.models import Sport, UnapprovedSport, UnapprovedSportComment
from excursions.models import Excursion, UnapprovedExcursion, UnapprovedExcursionComment
from entertainment.models import Entertainment, UnapprovedEntertainment, UnapprovedEntertainmentComment
from blog.models import UnapprovedBlogComment

from ..models import Service
from ..utils import build_country2prefix_dict, get_admin_changelist_url, get_absolute_url

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='divideby')
def divideby(value, arg):
    return value / (arg * 1.0)


@register.filter
def lookup(d, key):
    return d[key]


@register.filter("add_non_field_error_class")
@silence_without_field
def add_non_field_error_class(field, css_class):
    if hasattr(field.form, 'non_field_errors') and field.form.non_field_errors():
        return add_class(field, css_class)
    return field


@register.assignment_tag
def get_fb_app_id_if_any():
    try:
        fb_app = SocialApp.objects.get(provider=FacebookProvider.id)
        fb_app_id = fb_app.key
    except SocialApp.DoesNotExist:
        fb_app_id = None
    return fb_app_id


@register.simple_tag(name="get_current_absolute_url", takes_context=True)
def do_get_current_absolute_url(context, *args, **kwargs):
    request = context['request']
    return get_absolute_url(request, request.path)


@register.simple_tag(name="get_absolute_image_url", takes_context=True)
def do_get_absolute_image_url(context, image, *args, **kwargs):
    request = context['request']
    if kwargs.get('prepend_static', False):
        image = static(image)
    return get_absolute_url(request, image)

CONTRIB_MESSAGES_LEVEL_TO_NOTY_TYPE = {
    constants.INFO: 'info',
    constants.WARNING: 'warning',
    constants.ERROR: 'error',
    constants.SUCCESS: 'success'
}

@register.simple_tag
def contrib_messages_level_as_noty_type(message_level):
    return CONTRIB_MESSAGES_LEVEL_TO_NOTY_TYPE.get(message_level, 'warning')

@register.assignment_tag
def get_country2prefix_dict():
    return build_country2prefix_dict()


@register.assignment_tag
def hide_this_price_extra_form(forloop, subform, prices_initial_form_count):
    is_first = forloop['first']
    has_errors = bool(subform.errors)
    has_changed = subform.has_changed()
    show_it = has_changed or has_errors or (is_first and not prices_initial_form_count)
    return not show_it


@register.inclusion_tag('common/includes/services_info_table.html', takes_context=True)
def include_services_info_table(context):
    services = [Hotel, Apartment, Transport, Sport, Excursion, Entertainment]
    unapproved_services = [UnapprovedHotel, UnapprovedApartment, UnapprovedTransport, UnapprovedSport,
                           UnapprovedExcursion, UnapprovedEntertainment]
    unapproved_comments = [UnapprovedHotelComment, UnapprovedApartmentComment, UnapprovedTransportComment,
                           UnapprovedSportComment, UnapprovedExcursionComment, UnapprovedEntertainmentComment]
    unapproved_blog_comment = UnapprovedBlogComment
    names = []
    approved_numbers = []
    for service in services:
        names.append(service._meta.verbose_name_plural.title())
        approved_numbers.append(service.objects.filter(origin__isnull=True, status=Service.APPROVED).count())
    unapproved_infos = []
    for service in unapproved_services:
        count = service.objects.filter(origin__isnull=False, status=Service.ON_MODERATION).count()
        unapproved_infos.append({'count': count, 'link': get_admin_changelist_url(service)})
    no_prices_infos = []
    for service in services:
        count = service.objects.all().originals().has_no_prices().count()
        link = "%s?has_prices=no&type=1" % (get_admin_changelist_url(service))
        no_prices_infos.append({'count': count, 'link': link})
    unapproved_comment_infos = []
    for comment in unapproved_comments:
        unapproved_comment_infos.append({'count': comment.objects.count(), 'link': get_admin_changelist_url(comment)})

    unapproved_blog_comment_info = {
        'count': unapproved_blog_comment.objects.count(),
        'link': get_admin_changelist_url(unapproved_blog_comment)
    }

    return {
        'names': names,
        'approved_numbers': approved_numbers,
        'unapproved_infos': unapproved_infos,
        'no_prices_infos': no_prices_infos,
        'unapproved_comment_infos': unapproved_comment_infos,
        'unapproved_blog_comment_info': unapproved_blog_comment_info
    }


@register.filter('remove_newlines', is_safe=True)
@stringfilter
def do_remove_newlines(text):
    """
    Removes all newline characters from a block of text.
    """
    # First normalize the newlines using Django's nifty utility
    normalized_text = normalize_newlines(text)
    # Then simply remove the newlines like so.
    return mark_safe(normalized_text.replace('\n', ' '))


FACEBOOK_MAX_IMAGES = 5


@register.inclusion_tag('common/includes/fb_service_images_sharing.html', takes_context=True)
def fb_service_images_sharing(context, items1, items2=None):
    request = context['request']
    service = context['object']
    # service featured image always exists
    image_urls = [service.service_detail_big_featured_image()]
    # service gallery
    for img_obj in service.images.all():
        image_urls.append(img_obj.service_detail_big_image_thumbnail())
    if len(image_urls) < FACEBOOK_MAX_IMAGES:
        for item in items1:
            # items featured images
            if isinstance(item, Room):
                image_urls.append(item.featured_image_big_thumbnail())
            else:
                image_urls.append(item.find_service_big_image_thumbnail())
                # items gallery
                for img_obj in item.images.all():
                    image_urls.append(img_obj.find_service_big_image_thumbnail())
                if len(image_urls) >= FACEBOOK_MAX_IMAGES:
                    break
        else:
            if items2 is not None:
                # items featured images
                for item in items2:
                    image_urls.append(item.find_service_big_image_thumbnail())
                    # items gallery
                    for img_obj in item.images.all():
                        image_urls.append(img_obj.find_service_big_image_thumbnail())
                    if len(image_urls) >= FACEBOOK_MAX_IMAGES:
                        break

    if len(image_urls) > FACEBOOK_MAX_IMAGES:
        image_urls = image_urls[:FACEBOOK_MAX_IMAGES]

    image_urls = [get_absolute_url(request, image_url) for image_url in image_urls]
    return {'image_urls': image_urls}
