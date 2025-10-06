# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from copy import deepcopy
from easy_thumbnails.fields import ThumbnailerImageField
from hvad.models import TranslatableModel
from image_cropping import ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _, get_language
from multiselectfield import MultiSelectField

from users.models import User, BusinessOwnerInfo

from .utils import prepare_date


class ModeratableModel(TranslatableModel):
    ON_MODERATION, APPROVED, REJECTED, UPDATING = range(4)
    STATUSES = (
        (ON_MODERATION, _('On moderation')),  # model is shown for admin to approve if only it has this status
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (UPDATING, _('Updating')),  # intermediate status
    )
    duplicate = models.OneToOneField('self', verbose_name=_('Duplicate'), null=True, blank=True, related_name='origin',
                                     on_delete=models.SET_NULL)
    status = models.PositiveSmallIntegerField(verbose_name=_('Status'), choices=STATUSES, default=ON_MODERATION)
    # TODO: add reject_message to save why service was rejected and display it in business owner inteface.

    class Meta:
        abstract = True

    @classmethod
    def origin_pre_removal_step(cls, origin, duplicate, commit=False):
        raise NotImplementedError('Submodels should implement this method.')

    @classmethod
    def update_many2many_fields(cls, old_duplicate, new_duplicate):
        raise NotImplementedError('Submodels should implement this method.')

    @classmethod
    def rewrite_origin_object_with_approved_duplicate(cls, origin, duplicate):
        """
        :param origin:
        :param duplicate:
        :return:
        """
        origin_pk = origin.pk
        cls.origin_pre_removal_step(origin, duplicate)

        duplicate_pk = duplicate.pk
        # create copy of duplicate with origin pk
        duplicate.pk = origin_pk
        duplicate.save()
        old_dup = type(duplicate).objects.get(pk=duplicate_pk)

        cls.update_many2many_fields(old_dup, duplicate)
        old_dup.delete()

    @classmethod
    def remove_duplicate(cls, origin, duplicate):
        # cls.clear_many2many_fields(duplicate)
        duplicate.delete()
        origin.duplicate = None
        origin.save()

    status2css_class = {
        ON_MODERATION: 'pending',
        APPROVED: 'confirmed',
        REJECTED: 'rejected',
        UPDATING: 'pending'  # should not be used
    }

    def status_css_class(self):
        return self.status2css_class.get(self.status)

    def is_on_moderation(self):
        return self.status == self.ON_MODERATION

    def is_updating(self):
        return self.status == self.UPDATING

    def is_origin(self):
        return not self.has_origin()

    def is_duplicate(self):
        return self.has_origin()

    def has_origin(self):
        try:
            return self.origin is not None
        except ObjectDoesNotExist:
            return False

    def has_duplicate(self):
        return self.duplicate is not None

    def get_original(self):
        if self.is_duplicate():
            return self.origin
        else:
            return self

    def pre_save_custom_fields_duplication(self, copy):
        raise NotImplementedError('Submodels should implement this method.')

    def post_save_custom_fields_duplication(self, copy):
        raise NotImplementedError('Submodels should implement this method.')

    def create_object_duplicate_from_given(self):
        copy = deepcopy(self)
        copy.pk = None
        self.pre_save_custom_fields_duplication(copy)
        copy.save()
        self.post_save_custom_fields_duplication(copy)
        self.duplicate_id = copy.pk
        self.save()
        return copy


class Service(ModeratableModel):
    slug = models.SlugField(verbose_name=_('Slug'), max_length=255, unique=True)
    review_num = models.IntegerField(verbose_name=_('Review Number'), default=0)
    review_avg = models.FloatField(verbose_name=_('Review Average'), default=0.0)
    address = models.CharField(verbose_name=_('Address'), max_length=255, blank=True)
    featured_image = ThumbnailerImageField(verbose_name=_('Featured Image'), upload_to='uploads')
    big_crop = ImageRatioField('featured_image', '1000x600')
    small_crop = ImageRatioField('featured_image', '138x135')
    review_mode = models.BooleanField(default=False)  # is used to display services without prices on frontend

    details_url_name = None

    class Meta:
        abstract = True

    @models.permalink
    def get_absolute_url(self):
        if self.details_url_name is None:
            raise ImproperlyConfigured('Every service should declare "details_url_name".')
        return self.details_url_name, (), {'slug': self.slug}

    def has_prices(self):
        raise NotImplementedError('Submodels should implement this method.')

    def service_detail_big_featured_image(self):
        if self.featured_image:
            if self.big_crop:
                return cropped_thumbnail({}, self, 'big_crop')
            else:
                return self.featured_image['service_detail_page_big_image'].url

    def service_detail_small_featured_image(self):
        if self.featured_image:
            if self.small_crop:
                return cropped_thumbnail({}, self, 'small_crop')
            else:
                return self.featured_image['service_detail_page_small_image'].url

    def find_service_big_featured_image(self):
        return self.service_detail_big_featured_image()

    def find_service_small_featured_image(self):
        return self.service_detail_small_featured_image()

    def business_owner_page_featured_image_thumbnail(self):
        return self.featured_image['business_owner_page_image_preview'].url

    def generate_slug(self, commit=False):
        raise NotImplementedError('Service submodels should implement this method.')

    def recalculate_review_avg(self, new_review):
        self.review_avg = ((self.review_avg * self.review_num) + new_review) / (self.review_num + 1)
        self.review_num += 1
        self.save()


class Item(TranslatableModel):
    slug = models.SlugField(verbose_name=_('Slug'), max_length=255, unique=True)
    # title = models.CharField(verbose_name=_('Title'), max_length=255)
    # long_description = models.TextField(verbose_name=_('Long Description'), default="Sample description")
    # has_free_cancellation = models.BooleanField(verbose_name=_('Free cancellation'), default=False)

    class Meta:
        abstract = True


class ItemAndTimeBasedItem(Item):
    featured_image = ThumbnailerImageField(verbose_name=_('Image'), upload_to='uploads')
    crop = ImageRatioField('featured_image', '1000x600')
    cart_crop = ImageRatioField('featured_image', '170x120')
    price = models.FloatField(verbose_name=_('Price'), validators=[MinValueValidator(0.0)])

    number = models.PositiveSmallIntegerField(verbose_name=_('Number'), default=1)
    show_on_site = models.BooleanField(verbose_name=_('Show on site'), default=True)

    class Meta:
        abstract = True

    @property
    def is_item_based_item(self):
        raise ImproperlyConfigured('Every successor should define "is_item_based_item" property.')

    @property
    def is_time_based_item(self):
        raise ImproperlyConfigured('Every successor should define "is_time_based_item" property.')

    def calculate_price_for_booking(self, holiday_start, holiday_end, quantity=1):
        return self.calculate_total_price_and_price_per_day(holiday_start, holiday_end, quantity)[0]

    def calculate_total_price_and_price_per_day(self, holiday_start, holiday_end, quantity=1):
        if self.is_time_based_item:
            holiday_start = prepare_date(holiday_start)
            holiday_end = prepare_date(holiday_end)
            holiday_days = (holiday_end - holiday_start).days
            discount_price_object = self.discount_prices.filter(number_of_days__lte=holiday_days).order_by('-number_of_days').first()
            price = discount_price_object.discount_price if discount_price_object else self.price
            return price * holiday_days * quantity, price
        else:
            return self.price * quantity, self.price

    def find_service_big_image_thumbnail(self):
        if self.crop:
            return cropped_thumbnail({}, self, 'crop')
        else:
            return self.featured_image['service_detail_page_big_image'].url

    def service_detail_popup_image_thumbnail(self):
        return self.find_service_big_image_thumbnail()

    def service_detail_small_image_thumbnail(self):
        return self.find_service_big_image_thumbnail()

    def cart_image_thumbnail(self):
        if self.cart_crop:
            return cropped_thumbnail({}, self, 'cart_crop')
        else:
            return self.featured_image['cart_item_image'].url

    def business_owner_page_image_thumbnail(self):
        return self.featured_image['business_owner_page_image_preview'].url


class ItemPrice(models.Model):
    price = models.FloatField(verbose_name=_('Price'), validators=[MinValueValidator(0.0)])
    from_date = models.DateField(verbose_name=_('From Date'))
    to_date = models.DateField(verbose_name=_('To Date'))

    class Meta:
        abstract = True


class ThumbnailImage(models.Model):
    image = ThumbnailerImageField(verbose_name=_('Image'), upload_to='uploads')

    class Meta:
        abstract = True

class ServiceThumbnailImage(ThumbnailImage):
    big_crop = ImageRatioField('image', '1000x600')
    small_crop = ImageRatioField('image', '138x135')

    class Meta:
        abstract = True

    def service_detail_big_image_thumbnail(self):
        if self.big_crop:
            return cropped_thumbnail({}, self, 'big_crop')
        else:
            return self.image['service_detail_page_big_image'].url

    def service_detail_small_image_thumbnail(self):
        if self.small_crop:
            return cropped_thumbnail({}, self, 'small_crop')
        else:
            return self.image['service_detail_page_small_image'].url

    def find_service_big_image_thumbnail(self):
        return self.service_detail_big_image_thumbnail()

    def find_service_small_image_thumbnail(self):
        return self.service_detail_small_image_thumbnail()

    def business_owner_page_thumbnail(self):
        return self.image['business_owner_page_image_preview'].url


class ItemThumbnailImage(ThumbnailImage):
    crop = ImageRatioField('image', '1000x600')

    class Meta:
        abstract = True

    def service_detail_popup_image_thumbnail(self):
        if self.image:
            if self.crop:
                return cropped_thumbnail({}, self, 'crop')
            else:
                return self.image['service_detail_page_big_image'].url

    def find_service_big_image_thumbnail(self):
        return self.service_detail_popup_image_thumbnail()

    def business_owner_page_thumbnail(self):
        return self.image['business_owner_page_image_preview'].url


class ItemDiscountPrice(models.Model):
    number_of_days = models.SmallIntegerField(verbose_name=_('Number of days'), validators=[MinValueValidator(3),
                                                                                            MaxValueValidator(30)])
    # TODO: change floatfields to decimalfields in all models at the same time
    # discount_price = models.DecimalField(verbose_name=_('Discount price'), max_digits=9, decimal_places=2,
    #                                      validators=[MinValueValidator(Decimal('0.01'))])
    discount_price = models.FloatField(verbose_name=_('Discount price per day'), validators=[MinValueValidator(0.01)])

    class Meta:
        abstract = True

    @property
    def total(self):
        return self.number_of_days * self.discount_price


class DisplayableCommentsManager(models.Manager):
    def get_queryset(self):
        return super(DisplayableCommentsManager, self).get_queryset().filter(is_approved=True, language=get_language())


class AbstractComment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name=_('Text'))
    language = models.CharField(verbose_name=_('Language'), max_length=15, db_index=True, choices=settings.LANGUAGES,
                                default="en")
    is_approved = models.BooleanField(verbose_name=_('Is approved'), default=False)

    objects = models.Manager()
    displayable = DisplayableCommentsManager()

    class Meta:
        abstract = True


class Review(models.Model):
    RATE_CHOICES = ((x, x) for x in range(1, 6))
    rate = models.IntegerField(verbose_name=_('Rate'), choices=RATE_CHOICES)

    class Meta:
        abstract = True


class Language(models.Model):
    code = models.CharField(verbose_name=_('Code'), choices=settings.LANGUAGES, unique=True, max_length=10)
    is_enabled = models.BooleanField(verbose_name=_('Is enabled'), default=False)

    def __unicode__(self):
        return self.get_code_display()


def is_enabled_language(code):
    """
    Language model gives possibility to disable languages from settings.LANGUAGES but every language doesn't not have
    this instance necessarily so to decide that language is enabled we should check:
    1. if there is Language with that code it should have is_enabled flag equals True
    2. otherwise that code should just be listed in settings.LANGUAGES
    :param code: language code
    :return: True if the language with provided code is enabled
    """
    try:
        return Language.objects.get(code=code).is_enabled
    except Language.DoesNotExist:
        return code in settings.LANGUAGES_DICT


class TempFile(models.Model):
    image = ThumbnailerImageField(verbose_name='File', upload_to='uploads')
    created = models.DateTimeField(auto_now_add=True)

    def business_owner_page_thumbnail(self):
        return self.image['business_owner_page_image_preview'].url

    def __unicode__(self):
        return self.image.name

    class Meta:
        ordering = ('-created',)


@receiver(post_delete)
def post_delete_moderatable_model(sender, instance, *args, **kwargs):
    # Returns false if 'sender' is NOT a subclass of ModeratableModel
    if not issubclass(sender, ModeratableModel):
        return
    if instance.has_duplicate():
        instance.duplicate.delete()


class ReservationPhoneSettings(models.Model):
    phone = models.CharField(max_length=50)
    enabled_for_services = MultiSelectField(choices=BusinessOwnerInfo.SERVICE_TYPES,
                                            default=[service[0] for service in BusinessOwnerInfo.SERVICE_TYPES])
    is_enabled = models.BooleanField(default=True, help_text='Has the most priority. If set to False then '
                                                             'phone is not displayed at all regardless of '
                                                             '"enabled_for_services" field value')

    def __unicode__(self):
        return self.phone

    class Meta:
        verbose_name = verbose_name_plural = 'Reservation phone settings'
