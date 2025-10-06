from __future__ import unicode_literals
from easy_thumbnails.fields import ThumbnailerImageField
from hvad.manager import TranslationManager
from hvad.models import TranslatedFields
from uuslug import uuslug

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _, pgettext

from common.models import Service, Item, ThumbnailImage, ItemPrice, Review, AbstractComment, ServiceThumbnailImage, \
    ItemThumbnailImage, ItemDiscountPrice, ItemAndTimeBasedItem
from common.queryset_mixins import SimplePricesTranslationQueryset, SimplePricesFallbackQueryset, SimplePricesQueryset
from users.models import User


class ApprovedOriginExcursionsManager(TranslationManager):
    def get_queryset(self):
        return super(ApprovedOriginExcursionsManager, self).get_queryset().filter(origin__isnull=True,
                                                                                  status=Excursion.APPROVED)\
            .filter(Q(items__show_on_site=True) | Q(review_mode=True)).distinct()


class Excursion(Service):
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255),
        long_description=models.TextField(verbose_name=_('Description'))
    )
    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='excursions')

    details_url_name = 'view_excursion'

    objects = TranslationManager(queryset_class=SimplePricesTranslationQueryset,
                                 fallback_class=SimplePricesFallbackQueryset,
                                 default_class=SimplePricesQueryset)
    originals = ApprovedOriginExcursionsManager()

    class Meta:
        verbose_name = _('Excursion')
        verbose_name_plural = _('Excursions')

    def __unicode__(self):
        return self.title_trans

    def one_time_items(self):
        return self.items.filter(type=ExcursionItem.ONE_TIME)

    def tour_items(self):
        return self.items.filter(type=ExcursionItem.TOUR)

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


class UnapprovedExcursion(Excursion):

    class Meta:
        proxy = True
        verbose_name = _('Excursion (unapproved)')
        verbose_name_plural = _('Excursions (unapproved)')


class ExcursionImage(ServiceThumbnailImage):
    service = models.ForeignKey(Excursion, verbose_name=_('Excursion'), related_name='images')

    class Meta:
        verbose_name = _('Excursion Image')
        verbose_name_plural = _('Excursion Images')

    def __unicode__(self):
        return unicode(self.service_id)


class ExcursionReview(Review):
    service = models.ForeignKey(Excursion, verbose_name=_('Excursion'), related_name='reviews')
    reviewer = models.ForeignKey(User, verbose_name=_('Reviewer'), related_name='excursion_reviews')

    class Meta:
        unique_together = ('service', 'reviewer')


class ExcursionItem(ItemAndTimeBasedItem):
    ONE_TIME, TOUR = range(1, 3)
    TYPES = (
        (ONE_TIME, _('One Time')),
        (TOUR, _('Tour')),
    )
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_("Title"), max_length=255),
        long_description=models.TextField(verbose_name=_('Description'))
    )

    service = models.ForeignKey(Excursion, verbose_name=_('Excursion'), related_name="items")
    type = models.PositiveSmallIntegerField(verbose_name=_('Type'), choices=TYPES, default=ONE_TIME)

    shopping_cart_item_template = "excursions/includes/item_in_cart.html"

    class Meta:
        verbose_name = _('Excursion Item')
        verbose_name_plural = _('Excursion Items')

    def __unicode__(self):
        return self.title_trans

    def save(self, *args, **kwargs):
        remove_discount_prices = False
        if self.pk is not None:
            old_item_type = ExcursionItem.objects.get(pk=self.pk).type
            new_item_type = self.type
            if old_item_type != new_item_type and new_item_type == self.ONE_TIME:
                remove_discount_prices = True
        super(ExcursionItem, self).save(*args, **kwargs)
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
    def is_tour_item(self):
        return self.type == self.TOUR

    @property
    def is_item_based_item(self):
        return self.type == self.ONE_TIME

    @property
    def is_time_based_item(self):
        return self.type == self.TOUR

    def generate_slug(self, commit=False):
        self.slug = uuslug(self.title_trans, start_no=2, instance=self, max_length=255,
                           word_boundary=True)
        if commit:
            self.save()

    def orderitem_desc(self):
        return pgettext("excursion item description to display in end user booking tab",
                        'Item "%(item_type)s" in Excursion company '
                        '"%(excursion_name)s"' % {'item_type': self, 'excursion_name': self.service})

    # this method is required here to unify booking functionality for services with price categories and without
    # cause cartitem and orderitem contain different objects for them (price category in one case and service item in
    # another)
    def item(self):
        return self


class ExcursionItemImage(ItemThumbnailImage):
    service = models.ForeignKey(ExcursionItem, verbose_name=_('Excursion Item'), related_name='images')

    class Meta:
        verbose_name = _('Excursion Item Image')
        verbose_name_plural = _('Excursion Item Images')

    def __unicode__(self):
        return unicode(self.service_id)


class ExcursionItemDiscountPrice(ItemDiscountPrice):
    item = models.ForeignKey(ExcursionItem, verbose_name='Excursion Item', related_name='discount_prices')

    class Meta:
        ordering = ('number_of_days',)
        verbose_name = 'Excursion Item Discount Price'
        verbose_name_plural = 'Excursion Item Discount Prices'

    def __unicode__(self):
        return unicode(self.item_id)


class ExcursionComment(AbstractComment):
    entity = models.ForeignKey(Excursion, verbose_name=_('Excursion'), related_name='comments')
    creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='excursion_comments')

    def __unicode__(self):
        return u"{}'s comment".format(self.creator.email)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        unique_together = ('entity', 'creator')
        ordering = ('-created',)


# Use these models for admin only. Use ExcursionComment model to fetch comments for site.
class ApprovedExcursionCommentManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedExcursionCommentManager, self).get_queryset().filter(is_approved=True)


class ApprovedExcursionComment(ExcursionComment):
    objects = ApprovedExcursionCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (approved)')
        verbose_name_plural = _('Comments (approved)')


class UnapprovedExcursionCommentManager(models.Manager):
    def get_queryset(self):
        return super(UnapprovedExcursionCommentManager, self).get_queryset().filter(is_approved=False)


class UnapprovedExcursionComment(ExcursionComment):
    objects = UnapprovedExcursionCommentManager()

    class Meta:
        proxy = True
        verbose_name = _('Comment (unapproved)')
        verbose_name_plural = _('Comments (unapproved)')
