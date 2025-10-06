# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from aggregate_if import Min, Max
from skd_tools.mixins import ActiveTabMixin

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.utils.functional import cached_property
from django.utils.translation import pgettext_lazy
from django.views.generic import View, UpdateView, FormView, DetailView
from common.forms import DatetimeForm

from common.mixins import CommentList, JsonMixin, AjaxNewReviewMixin, \
    SetDatesAndGuestsIntoSessionMixin, AjaxNewServiceCommentMixin, ReservationPhoneToContextMixin
from common.utils import get_now_if_date_is_today_or_noon_of_that_date, get_noon_of_this_date, \
    get_arrival_from_session_or_default, get_departure_from_session_or_default
from users.mixins import EndUserOnlyMixin, BusinessOwnerOnlyMixin, BusinessProfileTabMixin
from users.models import BusinessOwnerInfo

from .forms import SportGalleryImageCropForm, SportFeaturedImageCropForm, SportItemGalleryImageCropForm, \
    SportItemImageCropForm, SportCommentForm, SportReviewForm, CartItemForm, SportSearchForm, ItemSearchForm
from .models import SportImage, Sport, SportItemImage, SportItem, SportComment, SportReview


class SportDetailView(SetDatesAndGuestsIntoSessionMixin, ReservationPhoneToContextMixin, ActiveTabMixin, DetailView):
    active_tab = 'sport'
    template_name = 'sports/sport_detail.html'
    ajax_template_name = 'sports/includes/ajax_sport_detail.html'
    ajax_template_name_time_based_only = 'sports/includes/ajax_sport_detail_time_based_only.html'
    queryset = Sport.objects.prefetch_related('images')
    comments_paginated_by = 10
    slug_field = 'slug__iexact'
    context_object_name = 'sport'
    business_type = BusinessOwnerInfo.SPORT

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super(SportDetailView, self).get_object(queryset)
        return self._object

    def get_template_names(self):
        if self.request.is_ajax():
            if 'update-time-based-booking-dates' in self.request.GET:
                return [self.ajax_template_name_time_based_only]
            else:
                return [self.ajax_template_name]
        else:
            return [self.template_name]

    # time-based is depended on choose dates values and GET parameters. This makes dates usage painful.
    # So I decided to separate them into (and check separately):
    # 1. item_based-from_date and item_based-to_date (taken from session only or week beginning from today)
    # 2. time_based-from_date and time_based-to_date (taken from GET params or equal to item_based dates)
    def get_context_data(self, **kwargs):
        context = super(SportDetailView, self).get_context_data(**kwargs)

        item_based_from_date = get_arrival_from_session_or_default(self.request)
        item_based_to_date = get_departure_from_session_or_default(self.request)
        valid_time_based_dates = True
        if 'time_based-arrival' in self.request.GET and 'time_based-departure' in self.request.GET:
            # there are some values for these fields so we should examine them
            form = ItemSearchForm(data=self.request.GET, prefix='time_based')
            if form.is_valid():
                time_based_from_date = form.cleaned_data['arrival']
                time_based_to_date = form.cleaned_data['departure']
            else:
                context['errors'] = [e for k, v in form.errors.items() for e in v]
                context['dates_form'] = form
                valid_time_based_dates = False
        else:
            time_based_from_date = item_based_from_date
            time_based_to_date = item_based_to_date

        if valid_time_based_dates:
            initial = {
                'arrival': time_based_from_date,
                'departure': time_based_to_date,
            }
            context['dates_form'] = ItemSearchForm(prefix='time_based', initial=initial)
            initial_cartitem = {
                'from_date': time_based_from_date,
                'to_date': time_based_to_date,
            }
            context['cartitem_form'] = CartItemForm(prefix='cartitem', initial=initial_cartitem)
            context['night_number'] = (time_based_to_date - time_based_from_date).days

        original = self.object.get_original()
        has_items = original.items.filter(show_on_site=True).exists()
        context['no_items'] = not has_items

        if has_items:
            # populate item-based items regardless of errors with dates for time-based items
            context['one_time_items'] = original.one_time_items().filter(show_on_site=True).prefetch_related(
                'images', 'translations')
            context['item_based_form_1'] = DatetimeForm(initial={'datetime': get_now_if_date_is_today_or_noon_of_that_date(item_based_from_date)})
            context['item_based_form_2'] = DatetimeForm(initial={'datetime': get_noon_of_this_date(item_based_to_date)})
            context['item_based_from_date'] = item_based_from_date
            context['item_based_to_date'] = item_based_to_date

            if valid_time_based_dates:
                # populate time-based items if only there are no errors with their dates
                context['time_based_from_date'] = time_based_from_date
                context['time_based_to_date'] = time_based_to_date
                context['subscription_items'] = original.subscription_items().filter(show_on_site=True).prefetch_related(
                    'images', 'translations', 'discount_prices')

        comments = SportComment.displayable.filter(entity_id=self.object.pk).select_related("creator")
        context['comments'] = comments[:self.comments_paginated_by]
        context['has_more_comments'] = comments.count() > self.comments_paginated_by
        context['can_add_comment'] = False
        context['can_review'] = False
        user = self.request.user
        if user.is_authenticated() and user.is_end_user() and not user.is_staff:
            has_comments_to_this_sport = self.request.user.sport_comments.filter(entity_id=self.object.pk).exists()
            context['can_add_comment'] = not has_comments_to_this_sport
            sport_review = self.request.user.sport_reviews.filter(service_id=self.object.pk).first()
            context['show_rate_block'] = True
            context['can_review'] = not sport_review
            if sport_review:
                context['user_review'] = sport_review.rate
        elif not user.is_authenticated():
            context['can_add_comment'] = True
            context['login_url'] = '{}?next={}?scroll=1'.format(reverse('account_login'), self.request.path)
        if context['can_add_comment']:
            initial_comment_form = {
                'entity_id': self.object.pk,
            }
            context['comment_form'] = SportCommentForm(prefix='comment', initial=initial_comment_form)
        return context

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        sport = self.get_object()
        staff_or_real_owner = user.is_authenticated() and (user.is_staff or (user.is_business_owner() and
                                                                             sport.owner == user))
        if staff_or_real_owner:
            if not request.is_ajax() and sport.status != Sport.APPROVED:
                messages.warning(request, pgettext_lazy('sport detail page not approved service warning message',
                                                        'This sport is not approved and can be viewed by you only.'))
        else:
            if not (sport.is_origin() and sport.status == Sport.APPROVED and
                    (sport.has_prices() or sport.review_mode)):
                raise Http404()
        return super(SportDetailView, self).dispatch(request, *args, **kwargs)


view_sport = SportDetailView.as_view()


class SportListView(SetDatesAndGuestsIntoSessionMixin, ActiveTabMixin, FormView):
    active_tab = 'sport'
    form_class = SportSearchForm
    template_name = 'sports/find_sport.html'
    ajax_list_only_template_name = 'sports/includes/ajax_find_sport_list_only.html'
    ajax_list_with_filters_template_name = 'sports/includes/ajax_find_sport_list_with_filters.html'
    paginated_by = 10

    def get_initial(self):
        initial = super(SportListView, self).get_initial()
        initial.update({
            'from_price': self.from_price,
            'to_price': self.to_price,
            'page': self.page,
            'type': self.type,
        })
        return initial

    def get_template_names(self):
        if self.request.is_ajax():
            if self.page > 1:
                return [self.ajax_list_only_template_name]
            else:
                return [self.ajax_list_with_filters_template_name]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super(SportListView, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        context['min_price'] = self.min_price
        context['max_price'] = self.max_price
        context['night_number'] = (self.date_to - self.date_from).days
        context['has_more_sports'] = self.has_more_sports
        return context

    @cached_property
    def type(self):
        return self.request.GET.getlist('type', [c[0] for c in SportItem.TYPES])

    def get_queryset(self):
        # filtering here is done on per item basis only (selected number of days is not taken into account)
        q = Sport.originals.all()
        q = q.annotate(min_price=Min('items__price',
                       only=(Q(items__show_on_site=True) &
                             Q(items__type__in=self.type))))
        if self.min_price != self.from_price or self.max_price != self.to_price:
            q = q.filter(Q(min_price__gte=self.from_price) & Q(min_price__lte=self.to_price) |
                         (Q(min_price__isnull=True) & Q(review_mode=True)))
        q = q.order_by('min_price')
        from_index = self.paginated_by * (self.page - 1)
        to_index = from_index + self.paginated_by
        self.has_more_sports = q.count() > to_index
        q = q[from_index:to_index].prefetch_related('translations', 'images')
        return q

    @cached_property
    def date_from(self):
        return get_arrival_from_session_or_default(self.request)

    @cached_property
    def date_to(self):
        return get_departure_from_session_or_default(self.request)

    @cached_property
    def price_range(self):
        price_range = SportItem.objects.filter(show_on_site=True, type__in=self.type).aggregate(min=Min('price'),
                                                                                                    max=Max('price'))
        if price_range['min'] and price_range['min'] == price_range['max']:
            price_range['max'] += 1

        return price_range

    @property
    def min_price(self):
        return self.price_range['min']

    @property
    def max_price(self):
        return self.price_range['max']

    @cached_property
    def from_price(self):
        if 'from_price' in self.request.GET:
            try:
                return float(self.request.GET['from_price'])
            except ValueError:
                pass
        return self.min_price

    @cached_property
    def to_price(self):
        if 'to_price' in self.request.GET:
            try:
                return float(self.request.GET['to_price'])
            except ValueError:
                pass
        return self.max_price

    @cached_property
    def page(self):
        if 'page' in self.request.GET:
            try:
                page = int(self.request.GET['page'])
            except ValueError:
                page = 1
        else:
            page = 1
        return page


find_sport = SportListView.as_view()


class AddItemsToCart(FormView):
    form_class = CartItemForm
    success_url = reverse_lazy('cart')
    prefix = 'cartitem'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('find_sport'))

    def form_invalid(self, form):
        if 'HTTP_REFERER' in self.request.META:
            failure_url = self.request.META['HTTP_REFERER']
        else:
            failure_url = reverse_lazy('explore')
        return HttpResponseRedirect(failure_url)

    def form_valid(self, form):
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')
        content_type = ContentType.objects.get_for_model(SportItem)
        for k, v in self.request.POST.items():
            if k.startswith("i_"):
                cat_pk = k.split("i_", 1)[1]
                quantity = int(v)
                if quantity > 0:
                    trans_item = SportItem.objects.get(pk=cat_pk)
                    object_id = trans_item.pk
                    if trans_item.is_one_time_item:
                        is_first_datetime_valid = False
                        first_datetime = self.request.POST.get('first_datetime_%s' % k)
                        if first_datetime:
                            datetime_form = DatetimeForm(data={'datetime': first_datetime})
                            if datetime_form.is_valid():
                                is_first_datetime_valid = True
                                first_datetime = datetime_form.cleaned_data['datetime']
                                self.request.cart.add_item(self.request, first_datetime, first_datetime, 1,
                                                           content_type, object_id, item_based_product=True)
                            if quantity == 2:
                                second_datetime = self.request.POST.get('second_datetime_%s' % k)
                                datetime_form = DatetimeForm(data={'datetime': second_datetime})
                                if datetime_form.is_valid():
                                    second_datetime = datetime_form.cleaned_data['datetime']
                                elif is_first_datetime_valid:
                                    second_datetime = first_datetime
                                else:
                                    continue
                                self.request.cart.add_item(self.request, second_datetime, second_datetime, 1,
                                                           content_type, object_id, item_based_product=True)
                    else:
                        if from_date and to_date:
                            self.request.cart.add_item(self.request, from_date, to_date, quantity, content_type, object_id)
        # quantity = form.cleaned_data['quantity']
        # object_id = form.cleaned_data['item_pk']
        # content_type_pk = form.cleaned_data['content_type_pk']
        # content_type = ContentType.objects.get(pk=content_type_pk)
        # self.request.cart.add_item(self.request, from_date, to_date, quantity, content_type, object_id)
        return super(AddItemsToCart, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_business_owner():
            return HttpResponseRedirect(reverse_lazy('business_profile'))
        return super(AddItemsToCart, self).dispatch(request, *args, **kwargs)


add_items_to_cart = AddItemsToCart.as_view()


class SportGalleryImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "sports/includes/ajax_sport_gallery_image_crop.html"
    tab_name = "service"
    model = SportImage
    form_class = SportGalleryImageCropForm
    success_url = reverse_lazy('update_service')

    def form_valid(self, form):
        """
        It's required to explicitly change sport status so that this changes will be visible and could be
        approved by admin.
        """
        self.object = form.save()
        if self.object.service.status == Sport.UPDATING:
            self.object.service.status = Sport.ON_MODERATION
            self.object.service.save()
        return super(SportGalleryImageCropView, self).form_valid(form)

sport_gallery_image_crop = SportGalleryImageCropView.as_view()


class SportFeaturedImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "sports/includes/ajax_sport_featured_image_crop.html"
    tab_name = "service"
    model = Sport
    form_class = SportFeaturedImageCropForm
    success_url = reverse_lazy('update_service')

    def form_valid(self, form):
        """
        It's required to explicitly change sport status so that this changes will be visible and could be
        approved by admin.
        """
        self.object = form.save(commit=False)
        if self.object.status == Sport.UPDATING:
            self.object.status = Sport.ON_MODERATION
        self.object.save()
        return super(SportFeaturedImageCropView, self).form_valid(form)


sport_featured_image_crop = SportFeaturedImageCropView.as_view()


class SportItemGalleryCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "sports/includes/ajax_sport_item_gallery_image_crop.html"
    tab_name = "service"
    model = SportItemImage
    form_class = SportItemGalleryImageCropForm

    def get_success_url(self):
        return reverse('update_item', kwargs={"slug": self.object.service.slug})

sport_item_gallery_image_crop = SportItemGalleryCropView.as_view()


class SportItemImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "sports/includes/ajax_sport_item_image_crop.html"
    tab_name = "service"
    model = SportItem
    form_class = SportItemImageCropForm

    def get_success_url(self):
        return reverse('update_item', kwargs={"slug": self.object.slug})

sport_item_image_crop = SportItemImageCropView.as_view()


class RemoveItemView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):

        data = {}

        item_slug = kwargs.get('slug', None)
        if item_slug:
            try:
                item = request.user.get_original_service().items.get(slug__iexact=item_slug)
            except SportItem.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no item with this slug.'
            else:
                item.delete()
                data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect item slug'

        return JsonResponse(data)


remove_item = RemoveItemView.as_view()


class ItemShowOnSiteAttrEditView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):

        data = {}

        item_slug = kwargs.get('slug', None)
        if item_slug:
            try:
                item = request.user.get_original_service().items.get(slug__iexact=item_slug)
            except SportItem.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no item with this slug.'
            else:
                show_on_site = request.POST.get('enable')
                new_val = True if show_on_site == "" else False
                if item.show_on_site != new_val:
                    item.show_on_site = new_val
                    item.save()
                data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect item slug'

        return JsonResponse(data)


item_show_on_site_attr_change = ItemShowOnSiteAttrEditView.as_view()


class ItemNumberAttrEditView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):

        data = {}

        new_val_str = request.POST.get("val")

        try:
            new_val = int(new_val_str)
        except ValueError:
            new_val = None

        if new_val is not None and new_val >= 0:
            item_slug = kwargs.get('slug', None)
            if item_slug:
                try:
                    item = request.user.get_original_service().items.get(slug__iexact=item_slug)
                except SportItem.DoesNotExist:
                    data['status'] = 'fail'
                    data['message'] = 'There is no sport item with this slug.'
                else:
                    if item.number != new_val:
                        item.number = new_val
                        item.save()
                    data['status'] = 'success'
            else:
                data['status'] = 'fail'
                data['message'] = 'Incorrect item slug'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect params'

        return JsonResponse(data)


item_number_attr_change = ItemNumberAttrEditView.as_view()


class NewSportCommentView(EndUserOnlyMixin, AjaxNewServiceCommentMixin, View):
    form_class = SportCommentForm
    model = SportComment

new_sport_comment = NewSportCommentView.as_view()


class SportCommentList(CommentList, View):
    ajax_template_name = "sports/comment_list.html"
    model = SportComment
    paginated_by = 20


comment_list = SportCommentList.as_view()


class NewSportReviewView(EndUserOnlyMixin, AjaxNewReviewMixin, View):
    ajax_template_name = "sports/includes/ajax_review_block.html"
    service_model = Sport
    review_model = SportReview
    form_class = SportReviewForm

new_sport_review = NewSportReviewView.as_view()
