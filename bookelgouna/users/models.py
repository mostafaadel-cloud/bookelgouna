# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_countries.fields import CountryField
from easy_thumbnails.fields import ThumbnailerImageField
from image_cropping import ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from .exceptions import BusinessOwnerOnly


class Country(models.Model):
    name = CountryField(verbose_name=pgettext_lazy('admin interface', 'Name'), unique=True)
    default_language = models.CharField(choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, max_length=2)

    def __unicode__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ('pk',)


class User(AbstractUser):
    END_USER = 1
    BUSINESS_OWNER = 2
    TRAVEL_AGENCY = 3

    STATUS_CHOICES = (
        (END_USER, _('End User')),
        (BUSINESS_OWNER, _('Business Owner')),
        (TRAVEL_AGENCY, 'Travel Agency')
    )

    type = models.PositiveIntegerField(verbose_name=pgettext_lazy('admin interface', 'Type'), choices=STATUS_CHOICES,
                                       default=END_USER, null=True, blank=True)
    avatar = ThumbnailerImageField(verbose_name=pgettext_lazy('admin interface', 'Avatar'), upload_to='uploads',
                                   blank=True)
    cropping = ImageRatioField('avatar', verbose_name=pgettext_lazy('admin interface', 'Cropping'),
                               size='118x118')  # size is "width x height"
    country = CountryField(blank=True, verbose_name=pgettext_lazy('admin interface', 'Country'))
    phone = PhoneNumberField(verbose_name=pgettext_lazy('admin interface', 'Phone'), null=True, blank=True)
    preferred_language = models.CharField(verbose_name=pgettext_lazy('admin interface', 'Language'),
                                          choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE, max_length=2)

    # start fields related to travel agency users
    base_account = models.ForeignKey('self', null=True, blank=True, related_name='subaccounts')
    # end

    class Meta:
        verbose_name = pgettext_lazy('admin interface', 'User')
        verbose_name_plural = pgettext_lazy('admin interface', 'Users')

    REQUIRED_FIELDS = ['email']

    def is_end_user(self):
        return self.type == User.END_USER

    def is_business_owner(self):
        return self.type == User.BUSINESS_OWNER

    def is_travel_agency(self):
        return self.type == User.TRAVEL_AGENCY

    def is_business_related_user(self):
        return self.type in [User.BUSINESS_OWNER, User.TRAVEL_AGENCY]

    def is_hotel_owner(self):
        return self.service_type == BusinessOwnerInfo.HOTEL

    def is_apt_owner(self):
        return self.service_type == BusinessOwnerInfo.APARTMENT

    def is_transport_owner(self):
        return self.service_type == BusinessOwnerInfo.TRANSPORT

    def is_excursions_owner(self):
        return self.service_type == BusinessOwnerInfo.EXCURSION

    def is_sports_owner(self):
        return self.service_type == BusinessOwnerInfo.SPORT

    def is_entertainment_owner(self):
        return self.service_type == BusinessOwnerInfo.ENTERTAINMENT

    def get_base_account_or_self(self):
        if self.is_business_owner():
            base_account = self.base_account
            if base_account:
                return base_account
        return self

    @cached_property
    def service_type(self):
        if not self.is_business_owner():
            raise BusinessOwnerOnly()
        return self.business_info.service_type

    def get_service_type_full_name(self):
        if not self.is_business_owner():
            raise BusinessOwnerOnly()
        return self.business_info.get_service_type_display()

    @cached_property
    def services_manager(self):
        if not self.is_business_owner():
            raise BusinessOwnerOnly()
        if self.is_hotel_owner():
            return self.hotels
        elif self.is_apt_owner():
            return self.apartments
        elif self.is_transport_owner():
            return self.transports
        elif self.is_sports_owner():
            return self.sports
        elif self.is_excursions_owner():
            return self.excursions
        elif self.is_entertainment_owner():
            return self.entertainments

    def has_service(self):
        return self.services_manager.exists()

    def get_original_service(self):
        return self.services_manager.get(origin__isnull=True)  # duplicate__isnull=True

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        else:
            return self.username

    def avatar_thumbnail(self):
        if self.avatar:
            if self.cropping:
                return cropped_thumbnail({}, self, 'cropping')
            else:
                return self.avatar['avatar_image'].url

    def show_next_link(self):
        return self.business_info.show_next_link

    def hide_next_link(self):
        if self.business_info.show_next_link:
            self.business_info.show_next_link = False
            self.business_info.save()


class BusinessOwnerInfo(models.Model):
    ALL_TYPES = HOTEL, APARTMENT, TRANSPORT, EXCURSION, SPORT, ENTERTAINMENT, AGENCY = range(7)

    SERVICE_TYPES = [
        (HOTEL, pgettext_lazy('admin interface and business owner interface tab name', 'Hotel')),
        (APARTMENT, pgettext_lazy('admin interface and business owner interface tab name', 'Apartment')),
        (TRANSPORT, pgettext_lazy('admin interface and business owner interface tab name', 'Transport')),
        (EXCURSION, pgettext_lazy('admin interface and business owner interface tab name', 'Excursion')),
        (SPORT, pgettext_lazy('admin interface and business owner interface tab name', 'Sport')),
        (ENTERTAINMENT, pgettext_lazy('admin interface and business owner interface tab name', 'Entertainment'))
    ]

    SERVICE_TYPES_AND_AGENCY = tuple(SERVICE_TYPES) + ((AGENCY, 'Agency'),)

    user = models.OneToOneField(User, primary_key=True, verbose_name=pgettext_lazy('admin interface', 'User'),
                                related_name='business_info')
    service_type = models.PositiveSmallIntegerField(verbose_name=pgettext_lazy('admin interface', 'Service Type'),
                                                    choices=SERVICE_TYPES)
    # "Next" link in profile redirects service owner to specific "create service" tab. we want to show it only at the
    # very beginning of site usage. so once he got access somehow to this tab this link is no more displayable.
    show_next_link = models.BooleanField(verbose_name=pgettext_lazy('admin interface', 'Show "Next" link in profile'),
                                         default=True)
    allowed_types = MultiSelectField(choices=SERVICE_TYPES, null=True, blank=True)

    class Meta:
        verbose_name = pgettext_lazy('admin interface', 'BusinessOwnerInfo')
        verbose_name_plural = pgettext_lazy('admin interface', 'BusinessOwnerInfos')
