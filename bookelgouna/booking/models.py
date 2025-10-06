# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import defaultdict
import random

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import ugettext_lazy as _, pgettext, pgettext_lazy
from apartments.models import ApartmentPriceCategory
from email_templates.models import BookingEmailTemplate
from entertainment.models import EntertainmentItem
from excursions.models import ExcursionItem

from hotels.models import Room, RoomPriceCategory
from sports.models import SportItem
from transport.models import TransportItem
from users.models import User


class CartManager(Manager):

    def get_queryset(self):
        queryset = super(CartManager, self).get_queryset()
        queryset = queryset.prefetch_related('items')
        return queryset

    def get_cart_from_request(self, request):
        if request.user.is_authenticated():
            try:
                return request.user.cart
            except Cart.DoesNotExist:
                default_key = '{}_{}'.format(request.user.id, random.random())
                cart, created = self.get_or_create(session_key=request.session.get('cart_key', '-1'))
                cart.user = request.user
                cart.session_key = default_key
                cart.save()
                request.cart = cart
                return cart

        if not request.session.session_key:
            request.session.create()
        cart, created = self.get_or_create(session_key=request.session.session_key)
        request.session['cart_key'] = request.session.session_key
        request.cart = cart
        return cart


class Cart(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='cart', null=True)
    # Session key is used to create and store cart for unsigned users
    # When user signs up we set up profile for cart and user can work with the same cart
    session_key = models.CharField(_('session key'), max_length=40, blank=True, unique=True)

    objects = CartManager()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def add_item(self, request, from_date, to_date, quantity, content_type, object_id, item_based_product=False):
        """
        Item based products are not updated using this method but added every time.
        """
        if not self.pk:
            self.save()
            request.session['cart'] = self.pk
        if item_based_product:
            self.items.create(content_type=content_type, object_id=object_id, from_date=from_date, to_date=to_date,
                              quantity=quantity, item_based_product=item_based_product)
        else:
            defaults = {'cart': self, 'from_date': from_date, 'to_date': to_date, 'quantity': quantity}
            self.items.update_or_create(content_type=content_type, object_id=object_id, defaults=defaults)

    def hotel_rooms(self):
        ct = ContentType.objects.get_for_model(RoomPriceCategory)
        return self.items.filter(content_type=ct).prefetch_related("content_object__translations",
                                                                   "content_object__item__translations")

    def apartments(self):
        ct = ContentType.objects.get_for_model(ApartmentPriceCategory)
        return self.items.filter(content_type=ct).prefetch_related("content_object__translations",
                                                                   "content_object__item__translations")

    def transport(self):
        ct = ContentType.objects.get_for_model(TransportItem)
        return self.items.filter(content_type=ct).prefetch_related("content_object__translations")

    def sports(self):
        ct = ContentType.objects.get_for_model(SportItem)
        return self.items.filter(content_type=ct).prefetch_related("content_object__translations")

    def excursions(self):
        ct = ContentType.objects.get_for_model(ExcursionItem)
        return self.items.filter(content_type=ct).prefetch_related("content_object__translations")

    def entertainment(self):
        ct = ContentType.objects.get_for_model(EntertainmentItem)
        return self.items.filter(content_type=ct).prefetch_related("content_object__translations")

    def total_price_for_cts(self):
        totals = defaultdict(float)
        for cart_item in self.items.all():
            item = cart_item.content_object
            from_date = cart_item.from_date
            to_date = cart_item.to_date
            qty = cart_item.quantity
            item_price_for_period = item.calculate_price_for_booking(from_date, to_date, qty)
            totals[cart_item.content_type] += item_price_for_period
        return totals

    def total_price(self):
        total = 0
        for cart_item in self.items.all():
            item = cart_item.content_object
            from_date = cart_item.from_date
            to_date = cart_item.to_date
            qty = cart_item.quantity
            item_price_for_period = item.calculate_price_for_booking(from_date, to_date, qty)
            total += item_price_for_period
        return total

    def in_cart(self, price_cat):
        try:
            return self.items.get(content_type=ContentType.objects.get_for_model(price_cat),
                                  object_id=price_cat.pk)
        except ObjectDoesNotExist:
            return None


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'), related_name='items')
    # limit = models.Q(app_label='hotels', model='room') | \
    #     models.Q(app_label='miapp', model='article')
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content page'),
        # limit_choices_to=limit,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('related object'),
        null=True,
    )
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    from_date = models.DateTimeField(verbose_name=_('From Date'))
    to_date = models.DateTimeField(verbose_name=_('To Date'))
    quantity = models.IntegerField(verbose_name=_('Quantity'), default=0)
    item_based_product = models.BooleanField(verbose_name=_('Item Based Product'), default=False)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')


class Order(models.Model):
    PENDING, CONFIRMED, REJECTED = range(1, 4)
    STATUS_CHOICES = (
        (PENDING, _('Pending')),
        (CONFIRMED, _('Confirmed')),
        (REJECTED, _('Rejected'))
    )
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='orders', blank=True, null=True,
                             on_delete=models.SET_NULL)
    total_price = models.FloatField(verbose_name=_('Total Price'), default=0.0, validators=[MinValueValidator(0.0)])
    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def complete(self, request):
        request.cart.delete()
        del request.session['cart']


class OrderItem(models.Model):
    PENDING, CONFIRMED, REJECTED, NO_SHOW, OFFLINE = range(1, 6)
    STATUS_CHOICES = (
        (PENDING, pgettext_lazy('business owner booking status', 'Pending')),
        (CONFIRMED, pgettext_lazy('business owner booking status', 'Confirmed')),
        (REJECTED, pgettext_lazy('business owner booking status', 'Rejected')),
        (NO_SHOW, pgettext_lazy('business owner booking status', 'No Show')),
        (OFFLINE, pgettext_lazy('business owner booking status', 'Offline'))
    )
    status2css = {
        PENDING: "pending",
        CONFIRMED: "confirmed",
        REJECTED: "rejected",
        NO_SHOW: "no_show",
        OFFLINE: "offline",
    }
    order = models.ForeignKey(Order, verbose_name=_('Order Item'), related_name='items')
    owner = models.ForeignKey(User, verbose_name=_('Owner'), related_name='order_items')
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content page'),
        # limit_choices_to=limit,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('related object'),
        null=True,
    )
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    item_desc = models.TextField(verbose_name=_('Item Description'))
    price = models.FloatField(verbose_name=_('Price'), default=0.0, validators=[MinValueValidator(0.0)])
    from_date = models.DateTimeField(verbose_name=_('From Date'))
    to_date = models.DateTimeField(verbose_name=_('To Date'))
    quantity = models.IntegerField(verbose_name=_('Quantity'), default=0)
    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=PENDING)
    # field to guarantee that noshow->confirmed->noshow status back and forth triggering can be done only once
    noshow_undo_done = models.BooleanField(verbose_name=_('No show undo done once'), default=False)
    item_based_product = models.BooleanField(verbose_name=_('Item Based Product'), default=False)
    offline_booking_note = models.TextField(verbose_name=_('Note'), blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Order Items')

    def save(self, *args, **kwargs):
        is_new_booking = False
        if self.pk is None:
            self.item_desc = self.content_object.orderitem_desc()
            is_new_booking = True
        super(OrderItem, self).save(*args, **kwargs)
        if is_new_booking and not self.is_offline():
            self.notify_owner_about_new_booking()

    def is_pending(self):
        return self.status == OrderItem.PENDING

    def is_offline(self):
        return self.status == OrderItem.OFFLINE

    def mark_as_offline(self, commit=True):
        self.status = OrderItem.OFFLINE
        if commit:
            self.save()

    def approve(self):
        if self.status == OrderItem.PENDING:
            self.status = OrderItem.CONFIRMED
            self.save()
            self.notify_owner_about_approval()
            self.notify_client_about_approval()

    def decline(self):
        if self.status == OrderItem.PENDING:
            self.status = OrderItem.REJECTED
            self.save()
            self.notify_owner_about_rejection()
            self.notify_client_about_rejection()

    def reject_due_to_owner_inactivity(self):
        if self.status == OrderItem.PENDING:
            self.status = OrderItem.REJECTED
            self.save()
            self.notify_owner_about_rejection_due_to_owner_inactivity()
            self.notify_client_about_rejection_due_to_owner_inactivity()
            return True
        else:
            return False

    def status_css_class(self):
        return self.status2css.get(self.status, "")

    @property
    def is_past_due(self):
        return timezone.now().date() > self.from_date.date()

    def is_hotel_room(self):
        return self.content_type == ContentType.objects.get_for_model(RoomPriceCategory)

    def is_apartment(self):
        return self.content_type == ContentType.objects.get_for_model(ApartmentPriceCategory)

    def is_transport(self):
        return self.content_type == ContentType.objects.get_for_model(TransportItem)

    def is_sport(self):
        return self.content_type == ContentType.objects.get_for_model(SportItem)

    def is_excursion(self):
        return self.content_type == ContentType.objects.get_for_model(ExcursionItem)

    def is_entertainment(self):
        return self.content_type == ContentType.objects.get_for_model(EntertainmentItem)

    def no_show_status_is_available(self):
        return self.status == OrderItem.CONFIRMED and (self.is_hotel_room() or self.is_apartment()) \
               and self.is_past_due and not self.noshow_undo_done

    def undo_action_is_available(self):
        return self.status == OrderItem.NO_SHOW and not self.noshow_undo_done

    def set_no_show_status(self):
        if self.status == OrderItem.CONFIRMED and self.is_past_due:
            self.status = OrderItem.NO_SHOW
            self.save()
            self.notify_owner_about_noshow()
            self.notify_client_about_noshow()

    def undo_no_show_status(self):
        if self.undo_action_is_available():
            self.status = OrderItem.CONFIRMED
            self.noshow_undo_done = True
            self.save()
            self.notify_owner_about_noshow_cancellation()
            self.notify_client_about_noshow_cancellation()

    def dates(self):
        if self.item_based_product:
            dates = pgettext('item based product booking dates to display in emails',
                             'Pick up on %(date)s' %
                             {'date': localtime(self.from_date).strftime('%d.%m.%Y %H:%M')})
        else:
            dates = pgettext('time based product booking dates to display in emails',
                             '%(from_date)s - %(to_date)s' %
                             {'from_date': localtime(self.from_date).strftime('%d.%m.%Y'),
                              'to_date': localtime(self.to_date).strftime('%d.%m.%Y')})
        return dates

    def notify_owner_about_new_booking(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_OWNER_ABOUT_NEW_BOOKING, self)

    def notify_owner_about_approval(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_OWNER_ABOUT_BOOKING_APPROVAL, self)

    def notify_client_about_approval(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_BOOKING_APPROVAL, self)

    def notify_owner_about_rejection(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_OWNER_ABOUT_BOOKING_MANUAL_REJECT, self)

    def notify_client_about_rejection(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_BOOKING_MANUAL_REJECT, self)

    def notify_owner_about_rejection_due_to_owner_inactivity(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_OWNER_ABOUT_BOOKING_AUTO_REJECT, self)

    def notify_client_about_rejection_due_to_owner_inactivity(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_BOOKING_AUTO_REJECT, self)

    def notify_owner_about_noshow(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_OWNER_ABOUT_NOSHOW_USED, self)

    def notify_client_about_noshow(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_NOSHOW_USED, self)

    def notify_owner_about_noshow_cancellation(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_OWNER_ABOUT_NOSHOW_CANCELLATION, self)

    def notify_client_about_noshow_cancellation(self):
        BookingEmailTemplate.objects.create_and_send_email_from_template_for_order_item(
            BookingEmailTemplate.NOTIFY_TOURIST_ABOUT_NOSHOW_CANCELLATION, self)

    def owner_phone(self):
        phone = self.owner.get_base_account_or_self().phone
        if phone:
            if self.status == OrderItem.CONFIRMED:
                return phone
            else:
                str_phone = str(phone)
                # replace part of the phone with X to hide it
                cut_phone = "{}{}".format(str_phone[:6], "X" * (len(str_phone) - 6))
                return cut_phone
        else:
            return _("No phone")

    def owner_email(self):
        email = self.owner.get_base_account_or_self().email
        if self.status == OrderItem.CONFIRMED:
            return email
        else:
            return _("Hidden")

    def end_user(self):
        return self.order.user

    def end_user_phone(self):
        if self.is_offline():
            return u'-'
        phone = self.order.user.phone
        if phone:
            if self.status == OrderItem.CONFIRMED:
                return phone
            else:
                str_phone = str(phone)
                # replace part of the phone with X to hide it
                cut_phone = "{}{}".format(str_phone[:6], "X" * (len(str_phone) - 6))
                return cut_phone
        else:
            return _("No phone")

    def end_user_email(self):
        if self.is_offline():
            return u'-'
        email = self.order.user.email
        if self.status == OrderItem.CONFIRMED:
            return email
        else:
            return _("Hidden")
