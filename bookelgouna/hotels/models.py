from __future__ import unicode_literals
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField
from hvad.manager import TranslationManager, TranslationQueryset, FallbackQueryset
from hvad.models import TranslatedFields, TranslatableModel
from image_cropping import ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail
from uuslug import uuslug

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Prefetch, Q, QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext

from common.models import Service, Item, ItemPrice, Review, AbstractComment, ServiceThumbnailImage
from common.utils import add_years, prepare_date
from users.models import User


class PricesMixin(object):
    def originals(self):
        return self.filter(origin__isnull=True)

    def duplicates(self):
        return self.filter(origin__isnull=False)

    def has_prices(self):
        return self.filter(Q(items__price_categories__isnull=False) |
                           Q(origin__items__price_categories__isnull=False)).distinct()

    def has_no_prices(self):
        return self.exclude(items__price_categories__isnull=False).exclude(
            origin__items__price_categories__isnull=False)


class PricesTranslationQueryset(PricesMixin, TranslationQueryset):
    pass


class PricesFallbackQueryset(PricesMixin, FallbackQueryset):
    pass


class PricesQueryset(PricesMixin, QuerySet):
    pass


class ApprovedOriginHotelsManager(TranslationManager):
    def get_queryset(self):
        return super(ApprovedOriginHotelsManager, self).get_queryset().filter(origin__isnull=True,
                                                                              status=Hotel.APPROVED).distinct()


class Hotel(Service):
    ONE_STAR, TWO_STARS, THREE_STARS, FOUR_STARS, FIVE_STARS = range(1, 6)

    HOTEL_RATINGS = (
        (ONE_STAR, _('One Star')),
        (TWO_STARS, _('Two Stars')),
        (THREE_STARS, _('Three Stars')),
        (FOUR_STARS, _('Four Stars')),
        (FIVE_STARS, _('Five Stars'))
    )

    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255),
        long_description=models.TextField(verbose_name=_('Description'))
    )
    rating = models.PositiveSmallIntegerField(verbose_name=_('Rating'), choices=HOTEL_RATINGS, default=FIVE_STARS)
    amenities = models.ManyToManyField("HotelAmenity", verbose_name=_("Amenities"), related_name="services")
    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='hotels')

    details_url_name = 'view_hotel'

    objects = TranslationManager(queryset_class=PricesTranslationQueryset, fallback_class=PricesFallbackQueryset,
                                 default_class=PricesQueryset)
    originals = ApprovedOriginHotelsManager()

    class Meta:
        verbose_name = _('Hotel')
        verbose_name_plural = _('Hotels')

    def __unicode__(self):
        return self.title_trans

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

    def has_prices(self):
        return self.items.filter(show_on_site=True).filter(price_categories__isnull=False).exists()

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


class HotelAmenityCategory(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(verbose_name=_("Name"), max_length=255, unique=True),
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    objects = TranslationManager()

    def __unicode__(self):
        return self.name_trans

    @property
    def name_trans(self):
        return self.lazy_translation_getter('name')

    class Meta:
        verbose_name = _('Hotel Amenity Category')
        verbose_name_plural = _('Hotel Amenity Categories')
        ordering = ('order',)


class HotelAmenity(TranslatableModel):
    category = models.ForeignKey(HotelAmenityCategory, verbose_name=_("Category"), related_name="amenities")
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
        verbose_name = _('Hotel Amenity')
        verbose_name_plural = _('Hotel Amenities')
        ordering = ('category__order',)


class UnapprovedHotel(Hotel):
    
    class Meta:
        proxy = True
        verbose_name = _('Hotel (unapproved)')
        verbose_name_plural = _('Hotels (unapproved)')


class HotelImage(ServiceThumbnailImage):
    service = models.ForeignKey(Hotel, verbose_name=_('Hotel'), related_name='images')

    class Meta:
        verbose_name = _('Hotel Image')
        verbose_name_plural = _('Hotel Images')

    def __unicode__(self):
        return unicode(self.service_id)


class HotelReview(Review):
    service = models.ForeignKey(Hotel, verbose_name=_('Hotel'), related_name='reviews')
    reviewer = models.ForeignKey(User, verbose_name=_('Reviewer'), related_name='hotel_reviews')

    class Meta:
        unique_together = ('service', 'reviewer')


class RoomType(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(verbose_name=_("Name"), max_length=50, unique=True),
    )

    def __unicode__(self):
        return self.name_trans

    @property
    def name_trans(self):
        return self.lazy_translation_getter('name')

    class Meta:
        verbose_name = _('Room Type')
        verbose_name_plural = _('Room Types')


class PrefetchPricesForDatesQueryset(models.QuerySet):
    def prefetch_prices_for_dates(self, from_date, to_date):
        return self.prefetch_related(Prefetch('price_categories',
                                              queryset=RoomPriceCategory.objects.filter(prices__isnull=False).distinct()))\
                    .prefetch_related(Prefetch('price_categories__prices',
                                              queryset=RoomPrice.objects.filter(
                                               Q(from_date__lte=from_date, to_date__gte=from_date) |
                                               Q(from_date__lte=to_date, to_date__gte=to_date) |
                                               Q(from_date__lte=from_date, to_date__gte=to_date) |
                                               Q(from_date__gte=from_date, to_date__lte=to_date)
                                               ).order_by('from_date')))


class PrefetchPricesForDatesManager(TranslationManager):

    def get_queryset(self):
        return PrefetchPricesForDatesQueryset(self.model, using=self._db).order_by("pk")

    def prefetch_prices_for_dates(self, from_date, to_date):
        return self.get_queryset().prefetch_prices_for_dates(from_date, to_date)


class Room(Item):
    translations = TranslatedFields(
        long_description=models.CharField(verbose_name=_('Room name'), max_length=50)
    )

    service = models.ForeignKey(Hotel, verbose_name=_('Hotel'), related_name="items")
    # type = models.ForeignKey(RoomType, verbose_name=_('Type'))
    area = models.FloatField(verbose_name=_('Area'), validators=[MinValueValidator(0.0)])
    featured_image = ThumbnailerImageField(verbose_name=_('Image'), upload_to='uploads')
    crop = ImageRatioField('featured_image', '170x120')
    adults = models.PositiveSmallIntegerField(verbose_name=_('Adults'), default=2,
                                              validators=[MinValueValidator(1)])
    children = models.PositiveSmallIntegerField(verbose_name=_('Children'), default=0)
    has_sea_views = models.BooleanField(verbose_name=_('Sea views'), default=False)
    has_air_conditioning = models.BooleanField(verbose_name=_('Air conditioning'), default=False)
    # is_breakfast_included = models.BooleanField(verbose_name=_('Breakfast included'), default=False)

    allotment = models.PositiveSmallIntegerField(verbose_name=_('Allotment'), default=1)
    show_on_site = models.BooleanField(verbose_name=_('Show on site'), default=True)

    amenities = models.ManyToManyField("RoomAmenity", verbose_name=_("Amenities"), related_name="items")

    shopping_cart_item_template = "hotels/includes/room_in_cart.html"

    objects = PrefetchPricesForDatesManager()

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __unicode__(self):
        return self.description_trans

    @property
    def owner(self):
        return self.service.owner

    @property
    def description_trans(self):
        return self.lazy_translation_getter('long_description')

    def generate_slug(self, commit=False):
        self.slug = uuslug(self.description_trans, start_no=2, instance=self, max_length=255,
                           word_boundary=True)
        if commit:
            self.save()

    def hotel_room_image_thumbnail(self):
        if self.featured_image:
            if self.crop:
                return cropped_thumbnail({}, self, 'crop')
            else:
                return self.featured_image['service_detail_page_item_image'].url

    def featured_image_big_thumbnail(self):
        """
        This thumbnail is used for facebook sharing only.
        :return: big thumbnail url
        """
        return self.featured_image['service_detail_page_big_image'].url

    def business_owner_page_image_thumbnail(self):
        return self.featured_image['business_owner_page_image_preview'].url

    def cart_image_thumbnail(self):
        return self.featured_image['cart_item_image'].url

    def orderitem_desc(self):
        return pgettext("hotel room description to display in end user booking tab",
                        'Room "%(room_type)s" (%(room_adults_num)d adults, %(room_child_num)d children) in Hotel "%(hotel_name)s"' %
                        {'room_type': self, 'room_adults_num': self.adults,
                         'room_child_num': self.children, 'hotel_name': self.service})


class DatesFilterQueryset(models.QuerySet):
    def filter_for_dates(self, from_date, to_date):
        return self.filter(
                           Q(from_date__lte=from_date, to_date__gte=from_date) |
                           Q(from_date__lte=to_date, to_date__gte=to_date) |
                           Q(from_date__lte=from_date, to_date__gte=to_date) |
                           Q(from_date__gte=from_date, to_date__lte=to_date)
                           ).order_by('from_date')


class MealPlan(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(verbose_name=_("Name"), max_length=255, unique=True),
    )

    def __unicode__(self):
        return self.name_trans

    @property
    def name_trans(self):
        return self.lazy_translation_getter('name')

    class Meta:
        verbose_name = _('Meal Plan')
        verbose_name_plural = _('Meal Plans')


class RoomPriceCategoryManager(TranslationManager):
    def get_queryset(self):
        return super(RoomPriceCategoryManager, self).get_queryset().order_by('-created')


class RoomPriceCategory(TranslatableModel):
    FREE_CANCELLATION = 1
    NON_REFUNDABLE = 2
    PAY_OPTION_CHOICES = (
        (FREE_CANCELLATION, _('Free Cancellation')),
        (NON_REFUNDABLE, _('Non Refundable'))
    )
    type = models.ForeignKey(RoomType, verbose_name=_('Type'))

    item = models.ForeignKey(Room, verbose_name=_('Room'), related_name="price_categories")

    regular_price = models.FloatField(verbose_name=_('Regular Price'), validators=[MinValueValidator(0.0)])

    pay_option = models.PositiveSmallIntegerField(verbose_name=_('Pay Option'), default=FREE_CANCELLATION,
                                                  choices=PAY_OPTION_CHOICES)

    meal_plan = models.ForeignKey(MealPlan, verbose_name=_("Meal Plan"))

    created = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        name=models.CharField(verbose_name=_('Category Name'), max_length=50),
        conditions=models.TextField(verbose_name=_('Conditions'))
    )

    shopping_cart_item_template = "hotels/includes/room_in_cart.html"

    objects = RoomPriceCategoryManager()

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
        verbose_name = _('Room Price Category')
        verbose_name_plural = _('Room Price Categories')

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
                    RoomPrice.objects.create(from_date=gen_range_start, to_date=gen_range_end, price=default,
                                             price_category=price_category, generated=True)
                    # next range should start from the end of current
                    gen_range_start = price_range.to_date

            # always ends with large range
            end = add_years(gen_range_start, 10)
            RoomPrice.objects.create(from_date=gen_range_start, to_date=end, price=default, price_category=price_category,
                                     generated=True)
        else:
            # one large range
            end = add_years(start, 10)
            RoomPrice.objects.create(from_date=start, to_date=end, price=default, price_category=price_category,
                                     generated=True)

    # these methods are required here to unify booking functionality for services with price categories and without
    # cause cartitem and orderitem contain different objects for them (price category in one case and service item in
    # another)
    @property
    def owner(self):
        return self.item.owner

    def orderitem_desc(self):
        return self.item.orderitem_desc()


class RoomPrice(ItemPrice):
    price_category = models.ForeignKey(RoomPriceCategory, verbose_name=_('Price Category'), null=True,
                                       related_name='prices')
    generated = models.BooleanField(default=False)

    objects = DatesFilterQueryset.as_manager()

    def __unicode__(self):
        return unicode(self.pk)

    class Meta:
        verbose_name = _('Room Price')
        verbose_name_plural = _('Room Prices')


# class RoomAmenityCategory(TranslatableModel):
#     translations = TranslatedFields(
#         name=models.CharField(verbose_name=_("Name"), max_length=255, unique=True),
#     )
#
#     def __unicode__(self):
#         return self.name_trans
#
#     @property
#     def name_trans(self):
#         return self.lazy_translation_getter('name')
#
#     class Meta:
#         verbose_name = _('Room Amenity Category')
#         verbose_name_plural = _('Room Amenity Categories')


class RoomAmenity(TranslatableModel):
    # items = models.ManyToManyField(Room, verbose_name=_("Rooms"), related_name="amenities")
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
        verbose_name = _('Room Amenity')
        verbose_name_plural = _('Room Amenities')


class HotelComment(AbstractComment):
    entity = models.ForeignKey(Hotel, verbose_name=_('Hotel'), related_name='comments')
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='hotel_comments')

    def __unicode__(self):
        return u"{}'s comment".format(self.creator.email)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        unique_together = ('entity', 'creator')
        ordering = ('-created',)


# Use these models for admin only. Use HotelComment model to fetch comments for site.
class ApprovedHotelCommentManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedHotelCommentManager, self).get_queryset().filter(is_approved=True)


class ApprovedHotelComment(HotelComment):
    objects = ApprovedHotelCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (approved)')
        verbose_name_plural = _('Comments (approved)')


class UnapprovedHotelCommentManager(models.Manager):
    def get_queryset(self):
        return super(UnapprovedHotelCommentManager, self).get_queryset().filter(is_approved=False)


class UnapprovedHotelComment(HotelComment):
    objects = UnapprovedHotelCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (unapproved)')
        verbose_name_plural = _('Comments (unapproved)')
