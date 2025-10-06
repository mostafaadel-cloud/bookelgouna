from __future__ import unicode_literals
from hvad.manager import TranslationManager, TranslationQueryset, FallbackQueryset
from hvad.models import TranslatedFields, TranslatableModel
from image_cropping import ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail
from uuslug import uuslug

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext

from common.models import Service, Item, ThumbnailImage, ItemPrice, Review, AbstractComment, ServiceThumbnailImage
from common.utils import add_years, prepare_date
from users.models import User



class PricesMixin(object):
    def originals(self):
        return self.filter(origin__isnull=True)

    def duplicates(self):
        return self.filter(origin__isnull=False)

    def has_prices(self):
        return self.filter(Q(price_category__isnull=False) | Q(origin__price_category__isnull=False)).distinct()

    def has_no_prices(self):
        return self.exclude(price_category__isnull=False).exclude(origin__price_category__isnull=False)


class PricesTranslationQueryset(PricesMixin, TranslationQueryset):
    pass


class PricesFallbackQueryset(PricesMixin, FallbackQueryset):
    pass


class PricesQueryset(PricesMixin, QuerySet):
    pass


class ApprovedOriginApartmentsWithPricesManager(TranslationManager):
    def get_queryset(self):
        return super(ApprovedOriginApartmentsWithPricesManager, self).get_queryset().filter(
            origin__isnull=True, status=Apartment.APPROVED, show_on_site=True).filter(Q(price_category__isnull=False) |
                                                                                      Q(review_mode=True)).distinct()


class Apartment(Service):
    APARTMENT, VILLA = range(1, 3)
    TYPES = (
        (APARTMENT, _('Apartment')),
        (VILLA, _('Villa')),
    )

    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255),
        long_description=models.TextField(verbose_name=_('Description'))
    )
    cart_crop = ImageRatioField('featured_image', '170x120')
    type = models.PositiveSmallIntegerField(verbose_name=_('Type'), choices=TYPES, default=APARTMENT)
    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='apartments')
    amenities = models.ManyToManyField("ApartmentAmenity", verbose_name=_("Amenities"), related_name="services")
    area = models.FloatField(verbose_name=_('Area'), validators=[MinValueValidator(0.0)], default=42.0)
    number_of_rooms = models.PositiveSmallIntegerField(verbose_name=_('Number of rooms'), default=1,
                                                       validators=[MinValueValidator(1)])
    min_nights_to_book = models.PositiveSmallIntegerField(verbose_name=_('Minimum number of nights to book'),
                                                          default=1, validators=[MinValueValidator(1)])
    adults = models.PositiveSmallIntegerField(verbose_name=_('Adults'), default=2,
                                              validators=[MinValueValidator(1)])
    children = models.PositiveSmallIntegerField(verbose_name=_('Children'), default=0)
    show_on_site = models.BooleanField(verbose_name=_('Show on site'), default=True)

    details_url_name = 'view_apartment'

    objects = TranslationManager(queryset_class=PricesTranslationQueryset, fallback_class=PricesFallbackQueryset,
                                 default_class=PricesQueryset)
    originals = ApprovedOriginApartmentsWithPricesManager()

    class Meta:
        verbose_name = _('Apartment')
        verbose_name_plural = _('Apartments')

    def __unicode__(self):
        return self.title_trans

    def is_villa(self):
        return self.type == self.VILLA

    def get_price_category(self):
        """
        always takes price category from original cause no need in moderation for this object
        :return: price category object if exists otherwise None
        """
        apt = self.get_original()
        try:
            return apt.price_category
        except ApartmentPriceCategory.DoesNotExist:
            return None

    def has_prices(self):
        return self.get_price_category() is not None

    def get_options(self):
        """
        always takes options from original cause no need in moderation for this object
        :return: options object if exists otherwise None
        """
        apt = self.get_original()
        try:
            return apt.options
        except ApartmentOptions.DoesNotExist:
            return None

    def non_empty_items(self):
        return self.items.filter(price_categories__isnull=False).distinct()

    @property
    def title_trans(self):
        return self.lazy_translation_getter('title')

    @property
    def description_trans(self):
        return self.lazy_translation_getter('long_description')

    def generate_slug(self, commit=False):
        self.slug = uuslug(self.title_trans, start_no=2, instance=self, max_length=255,
                           word_boundary=True)
        if commit:
            self.save()

    def cart_image_thumbnail(self):
        if self.featured_image:
            if self.cart_crop:
                return cropped_thumbnail({}, self, 'cart_crop')
            else:
                return self.featured_image['cart_item_image'].url

    def pre_save_custom_fields_duplication(self, copy):
        copy.translations_cache = None
        copy.slug = uuslug('duplicate', start_no=2, instance=self, max_length=255, word_boundary=True)

    def post_save_custom_fields_duplication(self, copy):
        for translation in self.translations.all():
            copy.translations.create(title=translation.title,
                                     long_description=translation.long_description,
                                     language_code=translation.language_code)
        for img in self.images.all():
            copy.images.create(image=img.image, big_crop=img.big_crop, small_crop=img.small_crop)
        for am in self.amenities.all():
            copy.amenities.add(am)

    @classmethod
    def origin_pre_removal_step(cls, origin, duplicate, commit=False):
        # remove unnecessary old m2ms
        origin.images.all().delete()
        origin.translations.all().delete()
        origin.amenities.clear()
        duplicate.slug = origin.slug
        duplicate.review_num = origin.review_num
        duplicate.review_avg = origin.review_avg
        if commit:
            duplicate.save()

    @classmethod
    def update_many2many_fields(cls, old_duplicate, new_duplicate):
        # reassign duplicate m2m fields to new copy with origin pk
        old_duplicate.translations.all().update(master=new_duplicate)
        old_duplicate.images.all().update(service=new_duplicate)
        for am in old_duplicate.amenities.all():
            new_duplicate.amenities.add(am)

    def orderitem_desc(self):
        return pgettext("apartment description to display in end user booking tab",
                        '%(apt_type)s "%(apt_name)s" (%(apt_rooms_num)d rooms, %(apt_adults_num)d adults, %(apt_child_num)d children)' %
                        {'apt_type': self.get_type_display(), 'apt_name': self, 'apt_rooms_num': self.number_of_rooms,
                         'apt_adults_num': self.adults, 'apt_child_num': self.children})


class UnapprovedApartment(Apartment):
    class Meta:
        proxy = True
        verbose_name = _('Apartment (unapproved)')
        verbose_name_plural = _('Apartments (unapproved)')


class ApartmentImage(ServiceThumbnailImage):
    service = models.ForeignKey(Apartment, verbose_name=_('Apartment'), related_name='images')

    class Meta:
        verbose_name = _('Apartment Image')
        verbose_name_plural = _('Apartment Images')

    def __unicode__(self):
        return unicode(self.service_id)


class ApartmentAmenity(TranslatableModel):
    # category = models.ForeignKey(RoomAmenityCategory, verbose_name=_("Category"), related_name="amenities")
    translations = TranslatedFields(
        name=models.CharField(verbose_name=_("Name"), max_length=255, unique=True),
    )

    objects = TranslationManager()

    def __unicode__(self):
        return self.name_trans

    @property
    def name_trans(self):
        return self.lazy_translation_getter('name')

    class Meta:
        verbose_name = _('Apartment Amenity')
        verbose_name_plural = _('Apartment Amenities')


class ApartmentReview(Review):
    service = models.ForeignKey(Apartment, verbose_name=_('Apartment'), related_name='reviews')
    reviewer = models.ForeignKey(User, verbose_name=_('Reviewer'), related_name='apartment_reviews')

    class Meta:
        unique_together = ('service', 'reviewer')


class DatesFilterQueryset(models.QuerySet):
    def filter_for_dates(self, from_date, to_date):
        return self.filter(
                           Q(from_date__lte=from_date, to_date__gte=from_date) |
                           Q(from_date__lte=to_date, to_date__gte=to_date) |
                           Q(from_date__lte=from_date, to_date__gte=to_date) |
                           Q(from_date__gte=from_date, to_date__lte=to_date)
                           ).order_by('from_date')


class ApartmentPriceCategoryManager(TranslationManager):
    def get_queryset(self):
        return super(ApartmentPriceCategoryManager, self).get_queryset().order_by('-created')


class ApartmentPriceCategory(TranslatableModel):
    FREE_CANCELLATION = 1
    NON_REFUNDABLE = 2
    PAY_OPTION_CHOICES = (
        (FREE_CANCELLATION, _('Free Cancellation')),
        (NON_REFUNDABLE, _('Non Refundable'))
    )

    item = models.OneToOneField(Apartment, verbose_name=_('Apartment'), related_name="price_category")

    regular_price = models.FloatField(verbose_name=_('Regular Price'), validators=[MinValueValidator(0.0)])

    pay_option = models.PositiveSmallIntegerField(verbose_name=_('Pay Option'), default=FREE_CANCELLATION,
                                                  choices=PAY_OPTION_CHOICES)

    created = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        name=models.CharField(verbose_name=_('Category Name'), max_length=255),
        conditions=models.TextField(verbose_name=_('Conditions'))
    )

    shopping_cart_item_template = "apartments/includes/apartment_in_cart.html"

    objects = ApartmentPriceCategoryManager()

    def __unicode__(self):
        return unicode(self.pk)

    @property
    def name_trans(self):
        return self.lazy_translation_getter('name')

    @property
    def conditions_trans(self):
        return self.lazy_translation_getter('conditions')

    def calculate_price_for_booking(self, holiday_start, holiday_end, quantity=1):
        holiday_start = prepare_date(holiday_start)
        holiday_end = prepare_date(holiday_end)
        s = holiday_start
        total_price = 0
        for price_range in self.prices.filter_for_dates(holiday_start, holiday_end):
            e = min([price_range.to_date, holiday_end])
            total_price += price_range.price * (e - s).days
            s = e
        return total_price * quantity

    def calculate_total_price_with_prefetched_prices(self, holiday_start, holiday_end, quantity=1):
        holiday_start = prepare_date(holiday_start)
        holiday_end = prepare_date(holiday_end)
        s = holiday_start
        total_price = 0
        for price_range in self.prices.all():
            e = min([price_range.to_date, holiday_end])
            total_price += price_range.price * (e - s).days
            s = e
        return total_price * quantity

    def manual(self):
        return self.prices.filter(generated=False)

    class Meta:
        verbose_name = _('Apartment Price Category')
        verbose_name_plural = _('Apartment Price Categories')

    @classmethod
    def generate_price_ranges_according_to_default(cls, price_category):
        for price in price_category.prices.filter(generated=True):
            price.delete()
        default = price_category.regular_price
        # nothing to do further if there is no regular price
        if default is None:
            return
        start = timezone.now().date()
        sorted_ranges = price_category.prices.filter(Q(from_date__lte=start, to_date__gt=start) |
                                                     Q(from_date__gt=start)).order_by('from_date')
        if sorted_ranges.exists():
            first_range = sorted_ranges.first()
            if first_range.from_date < start:
                gen_range_start = first_range.to_date
                sorted_ranges = sorted_ranges[1:]  # skip first range
            else:
                gen_range_start = start

            for price_range in sorted_ranges:
                if price_range.from_date == gen_range_start:
                    # no space to create range cause end of prev range is similar to start of next
                    gen_range_start = price_range.to_date
                else:
                    gen_range_end = price_range.from_date
                    ApartmentPrice.objects.create(from_date=gen_range_start, to_date=gen_range_end, price=default,
                                                  price_category=price_category, generated=True)
                    # next range should start from the end of current
                    gen_range_start = price_range.to_date

            # always ends with large range
            end = add_years(gen_range_start, 10)
            ApartmentPrice.objects.create(from_date=gen_range_start, to_date=end, price=default, price_category=price_category,
                                          generated=True)
        else:
            # one large range
            end = add_years(start, 10)
            ApartmentPrice.objects.create(from_date=start, to_date=end, price=default, price_category=price_category,
                                          generated=True)

    # these methods are required here to unify booking functionality for services with price categories and without
    # cause cartitem and orderitem contain different objects for them (price category in one case and service item in
    # another)
    @property
    def owner(self):
        return self.item.owner

    def orderitem_desc(self):
        return self.item.orderitem_desc()


class ApartmentPrice(ItemPrice):
    price_category = models.ForeignKey(ApartmentPriceCategory, verbose_name=_('Price Category'), null=True,
                                       related_name='prices')
    generated = models.BooleanField(default=False)

    objects = DatesFilterQueryset.as_manager()

    def __unicode__(self):
        return unicode(self.pk)

    class Meta:
        verbose_name = _('Apartment Price')
        verbose_name_plural = _('Apartment Prices')


class ApartmentOptions(models.Model):
    service = models.OneToOneField(Apartment, verbose_name='Apartment', related_name='options')
    for_long_term = models.BooleanField(verbose_name='For Long Term', default=False)
    long_term_price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])
    for_sale = models.BooleanField(verbose_name='For Sale', default=False)
    sale_price = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])

    class Meta:
        verbose_name = 'Apartment Option'
        verbose_name_plural = 'Apartment Options'

    def __unicode__(self):
        return "\"%s\" apt options" % self.service


class ApartmentComment(AbstractComment):
    entity = models.ForeignKey(Apartment, verbose_name=_('Apartment'), related_name='comments')
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='apartment_comments')

    def __unicode__(self):
        return u"{}'s comment".format(self.creator.email)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        unique_together = ('entity', 'creator')
        ordering = ('-created',)


# Use these models for admin only. Use ApartmentComment model to fetch comments for site.
class ApprovedApartmentCommentManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedApartmentCommentManager, self).get_queryset().filter(is_approved=True)


class ApprovedApartmentComment(ApartmentComment):
    objects = ApprovedApartmentCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (approved)')
        verbose_name_plural = _('Comments (approved)')


class UnapprovedApartmentCommentManager(models.Manager):
    def get_queryset(self):
        return super(UnapprovedApartmentCommentManager, self).get_queryset().filter(is_approved=False)


class UnapprovedApartmentComment(ApartmentComment):
    objects = UnapprovedApartmentCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (unapproved)')
        verbose_name_plural = _('Comments (unapproved)')
