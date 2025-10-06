from __future__ import unicode_literals
from hvad.manager import TranslationManager
from hvad.models import TranslatedFields
from uuslug import uuslug

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _, pgettext

from common.models import Service, ItemPrice, Review, AbstractComment, ServiceThumbnailImage, \
    ItemThumbnailImage, ItemDiscountPrice, ItemAndTimeBasedItem
from common.queryset_mixins import SimplePricesTranslationQueryset, SimplePricesFallbackQueryset, SimplePricesQueryset
from users.models import User


class ApprovedOriginSportsManager(TranslationManager):
    def get_queryset(self):
        return super(ApprovedOriginSportsManager, self).get_queryset().filter(origin__isnull=True,
                                                                              status=Sport.APPROVED)\
            .filter(Q(items__show_on_site=True) | Q(review_mode=True)).distinct()


class Sport(Service):
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255),
        long_description=models.TextField(verbose_name=_('Description'))
    )
    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='sports')

    details_url_name = 'view_sport'

    objects = TranslationManager(queryset_class=SimplePricesTranslationQueryset,
                                 fallback_class=SimplePricesFallbackQueryset,
                                 default_class=SimplePricesQueryset)
    originals = ApprovedOriginSportsManager()

    class Meta:
        verbose_name = _('Sport')
        verbose_name_plural = _('Sports')

    def __unicode__(self):
        return self.title_trans

    def one_time_items(self):
        return self.items.filter(type=SportItem.ONE_TIME)

    def subscription_items(self):
        return self.items.filter(type=SportItem.SUBSCRIPTION)

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
        return self.items.filter(show_on_site=True).exists()

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

    @classmethod
    def origin_pre_removal_step(cls, origin, duplicate, commit=False):
        # remove unnecessary old m2ms
        origin.images.all().delete()
        origin.translations.all().delete()
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


class UnapprovedSport(Sport):

    class Meta:
        proxy = True
        verbose_name = _('Sport (unapproved)')
        verbose_name_plural = _('Sports (unapproved)')


class SportImage(ServiceThumbnailImage):
    service = models.ForeignKey(Sport, verbose_name=_('Sport'), related_name='images')

    class Meta:
        verbose_name = _('Sport Image')
        verbose_name_plural = _('Sport Images')

    def __unicode__(self):
        return unicode(self.service_id)


class SportReview(Review):
    service = models.ForeignKey(Sport, verbose_name=_('Sport'), related_name='reviews')
    reviewer = models.ForeignKey(User, verbose_name=_('Reviewer'), related_name='sport_reviews')

    class Meta:
        unique_together = ('service', 'reviewer')


class SportItem(ItemAndTimeBasedItem):
    ONE_TIME, SUBSCRIPTION = range(1, 3)
    TYPES = (
        (ONE_TIME, _('One Time')),
        (SUBSCRIPTION, _('Subscription')),
    )
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255),
        long_description=models.TextField(verbose_name=_('Description'))
    )

    service = models.ForeignKey(Sport, verbose_name=_('Sport'), related_name="items")
    type = models.PositiveSmallIntegerField(verbose_name=_('Type'), choices=TYPES, default=ONE_TIME)

    shopping_cart_item_template = "sports/includes/item_in_cart.html"

    class Meta:
        verbose_name = _('Sport Item')
        verbose_name_plural = _('Sport Items')

    def __unicode__(self):
        return self.title_trans

    def save(self, *args, **kwargs):
        remove_discount_prices = False
        if self.pk is not None:
            old_item_type = SportItem.objects.get(pk=self.pk).type
            new_item_type = self.type
            if old_item_type != new_item_type and new_item_type == self.ONE_TIME:
                remove_discount_prices = True
        super(SportItem, self).save(*args, **kwargs)
        if remove_discount_prices:
            self.discount_prices.all().delete()

    @property
    def owner(self):
        return self.service.owner

    @property
    def title_trans(self):
        return self.lazy_translation_getter('title')

    @property
    def description_trans(self):
        return self.lazy_translation_getter('long_description')

    @property
    def is_one_time_item(self):
        return self.type == self.ONE_TIME

    @property
    def is_subscription_item(self):
        return self.type == self.SUBSCRIPTION

    @property
    def is_item_based_item(self):
        return self.type == self.ONE_TIME

    @property
    def is_time_based_item(self):
        return self.type == self.SUBSCRIPTION

    def generate_slug(self, commit=False):
        self.slug = uuslug(self.title_trans, start_no=2, instance=self, max_length=255,
                           word_boundary=True)
        if commit:
            self.save()

    def orderitem_desc(self):
        return pgettext("sport item description to display in end user booking tab",
                        'Item "%(item_type)s" in Sport company '
                        '"%(sport_name)s"' % {'item_type': self, 'sport_name': self.service})

    # this method is required here to unify booking functionality for services with price categories and without
    # cause cartitem and orderitem contain different objects for them (price category in one case and service item in
    # another)
    def item(self):
        return self


class SportItemImage(ItemThumbnailImage):
    service = models.ForeignKey(SportItem, verbose_name=_('Sport Item'), related_name='images')

    class Meta:
        verbose_name = _('Sport Item Image')
        verbose_name_plural = _('Sport Item Images')

    def __unicode__(self):
        return unicode(self.service_id)


class SportItemDiscountPrice(ItemDiscountPrice):
    item = models.ForeignKey(SportItem, verbose_name='Sport Item', related_name='discount_prices')

    class Meta:
        ordering = ('number_of_days',)
        verbose_name = 'Sport Item Discount Price'
        verbose_name_plural = 'Sport Item Discount Prices'

    def __unicode__(self):
        return unicode(self.item_id)


class SportComment(AbstractComment):
    entity = models.ForeignKey(Sport, verbose_name=_('Sport'), related_name='comments')
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='sport_comments')

    def __unicode__(self):
        return u"{}'s comment".format(self.creator.email)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        unique_together = ('entity', 'creator')
        ordering = ('-created',)


# Use these models for admin only. Use SportComment model to fetch comments for site.
class ApprovedSportCommentManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedSportCommentManager, self).get_queryset().filter(is_approved=True)


class ApprovedSportComment(SportComment):
    objects = ApprovedSportCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (approved)')
        verbose_name_plural = _('Comments (approved)')


class UnapprovedSportCommentManager(models.Manager):
    def get_queryset(self):
        return super(UnapprovedSportCommentManager, self).get_queryset().filter(is_approved=False)


class UnapprovedSportComment(SportComment):
    objects = UnapprovedSportCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (unapproved)')
        verbose_name_plural = _('Comments (unapproved)')
