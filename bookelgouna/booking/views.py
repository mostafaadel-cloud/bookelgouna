# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import pgettext
from django.views.generic import DetailView, View, TemplateView, UpdateView
from phonenumbers import format_number, example_number, PhoneNumberFormat

from apartments.models import ApartmentPriceCategory
from common.utils import get_phone_prefix_or_empty_string_for
from users.forms import EndUserAddPhoneForm
from users.models import User
from users.mixins import EndUserOnlyMixin, BusinessOwnerOnlyMixin
from users.utils import get_country_code_by_ip_using_geoip

from booking.tasks import reject_orderitem
from .models import Order, OrderItem
from .utils import get_order_item_with_this_item_in_dates


class CartView(DetailView):

    template_name = 'booking/cart.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart = self.request.cart
        context['category2total'] = cart.total_price_for_cts()
        context['total_amount'] = cart.total_price()
        return context

    def get_object(self, queryset=None):
        return self.request.cart

cart_view = CartView.as_view()


class CheckoutView(EndUserOnlyMixin, TemplateView):
    template_name = 'booking/checkout.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['total_amount'] = self.request.cart.total_price()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        if request.user.phone is None:
            return HttpResponseRedirect(reverse('checkout_enter_phone'))
        cart = request.cart
        order = Order.objects.create(user=user, total_price=cart.total_price())
        eta = timezone.now() + timedelta(hours=settings.BOOKING_REJECT_AFTER_HOURS_OF_INACTIVITY)
        for cart_item in cart.items.all():
            item = cart_item.content_object
            from_date = cart_item.from_date
            to_date = cart_item.to_date
            qty = cart_item.quantity
            item_price_for_period = item.calculate_price_for_booking(from_date, to_date, qty)
            item_based_product = cart_item.item_based_product
            # prevent from book apartment that is already booked on selected dates
            if not isinstance(item, ApartmentPriceCategory) or get_order_item_with_this_item_in_dates(item, from_date,
                                                                                                      to_date) is None:
                order_item = OrderItem.objects.create(order=order, content_object=item, price=item_price_for_period,
                                                      from_date=from_date, to_date=to_date, quantity=qty,
                                                      owner=item.owner, item_based_product=item_based_product)
                reject_orderitem.apply_async((order_item.pk,), eta=eta)
            cart_item.delete()
        cart.delete()
        delattr(request, '_cached_cart')
        return HttpResponseRedirect(reverse_lazy('user_bookings'))

    def dispatch(self, request, *args, **kwargs):
        if request.cart.items.exists():
            return super(CheckoutView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('explore'))


checkout = CheckoutView.as_view()


class CheckoutEnterPhoneView(EndUserOnlyMixin, UpdateView):
    model = User
    form_class = EndUserAddPhoneForm
    template_name = 'booking/checkout_enter_phone.html'
    success_url = reverse_lazy('checkout')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(CheckoutEnterPhoneView, self).get_context_data(**kwargs)
        context['phone_placeholder'] = pgettext('end user checkout phone example string',
                                                'i.e. %s' % format_number(example_number(self.form_class.COUNTRY_CODE),
                                                                          PhoneNumberFormat.E164))
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.phone is None and request.cart.items.exists():
            return super(CheckoutEnterPhoneView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('explore'))

checkout_enter_phone = CheckoutEnterPhoneView.as_view()


class ChangeOrderitemView(BusinessOwnerOnlyMixin, View):
    ajax_template_name = "booking/includes/ajax_business_profile_orderitem.html"

    def post(self, request, *args, **kwargs):

        data = {}

        action = request.POST.get('action')
        orderitem_pk = kwargs.get('pk', None)
        if orderitem_pk and action:
            try:
                orderitem = request.user.order_items.get(pk=orderitem_pk)
            except OrderItem.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no orderitem with this pk.'
            else:
                data['status'] = 'success'
                if action == '1':
                    orderitem.approve()
                elif action == '2':
                    orderitem.decline()
                elif action == '3':
                    orderitem.set_no_show_status()
                elif action == '4':
                    orderitem.undo_no_show_status()
                data['html'] = render_to_string(self.ajax_template_name, {'item': orderitem},
                                                context_instance=RequestContext(self.request)),
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect parameters'

        return JsonResponse(data)


change_orderitem = ChangeOrderitemView.as_view()


class DeleteCartitemView(View):

    def post(self, request, *args, **kwargs):

        data = {}

        cartitem_pk = kwargs.get('pk', None)
        if cartitem_pk:
            try:
                cartitem = request.cart.items.get(pk=cartitem_pk)
            except OrderItem.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no cartitem with this pk.'
            else:
                cartitem.delete()
                data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect parameters'

        return JsonResponse(data)


delete_cartitem = DeleteCartitemView.as_view()
