from aggregate_if import Min, Max
from braces.views import PrefetchRelatedMixin
from extra_views import CreateWithInlinesView, NamedFormsetsMixin, UpdateWithInlinesView
from skd_tools.mixins import ActiveTabMixin
import time

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q, Prefetch
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.utils.functional import cached_property
from django.utils.translation import pgettext_lazy
from django.views.generic import DetailView, FormView, View, UpdateView

from common.mixins import CommentList, JsonMixin, AjaxNewReviewMixin, \
    SetDatesAndGuestsIntoSessionMixin, AjaxNewServiceCommentMixin, ReservationPhoneToContextMixin
from common.utils import get_arrival_from_session_or_default, get_departure_from_session_or_default
from hotels.forms import HotelSearchForm, RoomSearchForm, RoomPriceCategoryTranslationsInline, \
    RoomPriceCategoryPricesInline
from users.mixins import BusinessOwnerOnlyMixin, EndUserOnlyMixin, BusinessProfileTabMixin
from users.models import BusinessOwnerInfo

from .forms import CartItemForm, HotelCommentForm, RoomPriceCategoryForm, HotelGalleryImageCropForm, \
    HotelFeaturedImageCropForm, RoomImageCropForm, HotelReviewForm
from .models import Hotel, RoomPrice, Room, HotelComment, HotelReview, RoomPriceCategory, \
    HotelImage


class HotelDetailView(SetDatesAndGuestsIntoSessionMixin, ReservationPhoneToContextMixin, ActiveTabMixin, DetailView):
    active_tab = 'hotels'
    template_name = 'hotels/hotel_detail.html'
    ajax_template_name = 'hotels/includes/ajax_hotel_detail.html'
    queryset = Hotel.objects.prefetch_related('images', 'amenities__translations', 'amenities__category__translations')
    comments_paginated_by = 10
    slug_field = 'slug__iexact'
    context_object_name = 'hotel'
    business_type = BusinessOwnerInfo.HOTEL

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super(HotelDetailView, self).get_object(queryset)
        return self._object

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super(HotelDetailView, self).get_context_data(**kwargs)

        if 'detail-arrival' in self.request.GET or 'detail-departure' in self.request.GET:
            # there are some values for these fields so we should examine them
            form = RoomSearchForm(data=self.request.GET, prefix='detail')
            if form.is_valid():
                from_date = form.cleaned_data['arrival']
                to_date = form.cleaned_data['departure']
            else:
                context['errors'] = [e for k, v in form.errors.items() for e in v]
                context['dates_form'] = form
        else:
            from_date = get_arrival_from_session_or_default(self.request)
            to_date = get_departure_from_session_or_default(self.request)

        context['has_prices'] = has_prices = self.object.has_prices()
        if 'errors' not in context:
            # adults = self.get_adults_from_session_or_default()
            # children = self.get_children_from_session_or_default()
            # filter(adults__gte=adults, children__gte=children)

            if has_prices:
                rooms = self.object.get_original().non_empty_items()
            else:
                rooms = self.object.get_original().items.all()
            rooms = rooms.filter(show_on_site=True)

            context['rooms'] = rooms.prefetch_prices_for_dates(from_date, to_date).prefetch_related(
                'translations',
                'price_categories__translations',
                'price_categories__type__translations',
                'price_categories__meal_plan__translations',
                'amenities__translations',
                )
            context['start_date'] = from_date
            context['end_date'] = to_date

        if 'dates_form' not in context:
            initial = {
                'arrival': from_date,
                'departure': to_date,
            }
            context['dates_form'] = RoomSearchForm(prefix='detail', initial=initial)
            initial_cartitem = {
                'from_date': from_date,
                'to_date': to_date,
                # 'content_type_pk': ContentType.objects.get_for_model(Room).pk
            }
            context['cartitem_form'] = CartItemForm(prefix='cartitem', initial=initial_cartitem)
            context['night_number'] = (to_date - from_date).days
        comments = HotelComment.displayable.filter(entity_id=self.object.pk).select_related("creator")
        context['comments'] = comments[:self.comments_paginated_by]
        context['has_more_comments'] = comments.count() > self.comments_paginated_by
        context['can_add_comment'] = False
        context['can_review'] = False
        user = self.request.user
        if user.is_authenticated() and user.is_end_user() and not user.is_staff:
            has_comments_to_this_hotel = self.request.user.hotel_comments.filter(entity_id=self.object.pk).exists()
            context['can_add_comment'] = not has_comments_to_this_hotel
            hotel_review = self.request.user.hotel_reviews.filter(service_id=self.object.pk).first()
            context['show_rate_block'] = True
            context['can_review'] = not hotel_review
            if hotel_review:
                context['user_review'] = hotel_review.rate
        elif not user.is_authenticated():
            context['can_add_comment'] = True
            context['login_url'] = '{}?next={}?scroll=1'.format(reverse('account_login'), self.request.path)
        if context['can_add_comment']:
            initial_comment_form = {
                'entity_id': self.object.pk,
            }
            context['comment_form'] = HotelCommentForm(prefix='comment', initial=initial_comment_form)
        return context

    def get_adults_from_session_or_default(self):
        return self.request.session.get('adults', 0)

    def get_children_from_session_or_default(self):
        return self.request.session.get('children', 0)

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        hotel = self.get_object()
        staff_or_real_owner = user.is_authenticated() and (user.is_staff or (user.is_business_owner() and
                                                                             hotel.owner == user))
        if staff_or_real_owner:
            if not request.is_ajax() and hotel.status != Hotel.APPROVED:
                messages.warning(request, pgettext_lazy('hotel detail page not approved service warning message',
                                                        'This hotel is not approved and can be viewed by you only.'))
        else:
            if not (hotel.is_origin() and hotel.status == Hotel.APPROVED and
                    (hotel.has_prices() or hotel.review_mode)):
                raise Http404()
        return super(HotelDetailView, self).dispatch(request, *args, **kwargs)


view_hotel = HotelDetailView.as_view()


class HotelListView(SetDatesAndGuestsIntoSessionMixin, ActiveTabMixin, FormView):
    active_tab = 'hotels'
    form_class = HotelSearchForm
    template_name = 'hotels/find_hotel.html'
    ajax_list_only_template_name = 'hotels/includes/ajax_find_hotel_list_only.html'
    ajax_list_with_filters_template_name = 'hotels/includes/ajax_find_hotel_list_with_filters.html'
    paginated_by = 10

    def get_initial(self):
        initial = super(HotelListView, self).get_initial()
        initial.update({
            'rating': self.get_rating(),
            'from_price': self.get_from_price(),
            'to_price': self.get_to_price(),
            'page': self.get_page()
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
        context = super(HotelListView, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        context['min_price'] = self.get_min_price()
        context['max_price'] = self.get_max_price()
        context['night_number'] = (self.get_to_date() - self.get_from_date()).days
        context['has_more_hotels'] = self.has_more_hotels
        return context

    def get_queryset(self):
        q = Hotel.originals.all()
        if self.get_rating() != Hotel.FIVE_STARS:
            q = q.filter(rating__lte=self.get_rating())
        first_day = self.get_from_date()
        q = q.annotate(price_per_night=Min('items__price_categories__prices__price',
                       only=(# Q(items__adults__gte=self.get_adults()) &
                             # Q(items__children__gte=self.get_children()) &
                             Q(items__show_on_site=True) &
                             Q(items__price_categories__prices__isnull=False) &
                             Q(items__price_categories__prices__from_date__lte=first_day) &
                             Q(items__price_categories__prices__to_date__gt=first_day))))\
            .filter(Q(price_per_night__isnull=False) | Q(review_mode=True))
        if self.get_min_price() != self.get_from_price() or self.get_max_price() != self.get_to_price():
            q = q.filter(Q(price_per_night__gte=self.from_price) & Q(price_per_night__lte=self.to_price) |
                         Q(price_per_night__isnull=True))
        q = q.order_by('price_per_night')
        from_index = self.paginated_by * (self.get_page() - 1)
        to_index = self.paginated_by * self.get_page()
        self.has_more_hotels = q.count() > to_index
        q = q[from_index:to_index].prefetch_related('translations', 'images')
        return q

    def get_rating(self):
        if not hasattr(self, 'rating'):
            if 'rating' in self.request.GET:
                self.rating = self.request.GET['rating']
            else:
                self.rating = Hotel.FIVE_STARS
        return self.rating

    def get_from_date(self):
        if not hasattr(self, 'from_date'):
            self.from_date = get_arrival_from_session_or_default(self.request)
        return self.from_date

    def get_to_date(self):
        if not hasattr(self, 'to_date'):
            self.to_date = get_departure_from_session_or_default(self.request)
        return self.to_date

    @cached_property
    def price_range(self):
        price_range = RoomPrice.objects.filter(
                           Q(from_date__lte=self.get_from_date(), to_date__gte=self.get_from_date()) |
                           Q(from_date__lte=self.get_to_date(), to_date__gte=self.get_to_date()) |
                           Q(from_date__lte=self.get_from_date(), to_date__gte=self.get_to_date()) |
                           Q(from_date__gte=self.get_from_date(), to_date__lte=self.get_to_date())).aggregate(min=Min('price'), max=Max('price'))

        if price_range['min'] and price_range['min'] == price_range['max']:
            price_range['max'] += 1

        if not price_range['min']:
            price_range = RoomPriceCategory.objects.aggregate(min=Min('regular_price'), max=Max('regular_price'))

        return price_range

    def get_min_price(self):
        return self.price_range['min']

    def get_max_price(self):
        return self.price_range['max']

    def get_from_price(self):
        if not hasattr(self, 'from_price'):
            if 'from_price' in self.request.GET:
                self.from_price = float(self.request.GET['from_price'])
            else:
                self.from_price = self.get_min_price()
        return self.from_price

    def get_to_price(self):
        if not hasattr(self, 'to_price'):
            if 'to_price' in self.request.GET:
                self.to_price = float(self.request.GET['to_price'])
            else:
                self.to_price = self.get_max_price()
        return self.to_price

    def get_adults(self):
        if not hasattr(self, 'adults'):
            if 'adults' in self.request.session:
                self.adults = self.request.session['adults']
            else:
                self.adults = 2
        return self.adults

    def get_children(self):
        if not hasattr(self, 'children'):
            if 'children' in self.request.session:
                self.children = self.request.session['children']
            else:
                self.children = 0
        return self.children

    def get_page(self):
        if not hasattr(self, 'page'):
            if 'page' in self.request.GET:
                try:
                    page = int(self.request.GET['page'])
                except ValueError:
                    page = 1
            else:
                page = 1
            self.page = page
        return self.page


find_hotel = HotelListView.as_view()


class AddRoomsToCart(FormView):
    form_class = CartItemForm
    success_url = reverse_lazy('cart')
    prefix = 'cartitem'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('find_hotel'))

    def form_invalid(self, form):
        if 'HTTP_REFERER' in self.request.META:
            failure_url = self.request.META['HTTP_REFERER']
        else:
            failure_url = reverse_lazy('explore')
        return HttpResponseRedirect(failure_url)

    def form_valid(self, form):
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        content_type = ContentType.objects.get_for_model(RoomPriceCategory)
        for k, v in self.request.POST.items():
            if k.startswith("pc_"):
                cat_pk = k.split("pc_", 1)[1]
                quantity = int(v)
                if quantity > 0:
                    price_category = RoomPriceCategory.objects.get(pk=cat_pk)
                    object_id = price_category.pk
                    self.request.cart.add_item(self.request, from_date, to_date, quantity, content_type, object_id)
        # quantity = form.cleaned_data['quantity']
        # object_id = form.cleaned_data['item_pk']
        # content_type_pk = form.cleaned_data['content_type_pk']
        # content_type = ContentType.objects.get(pk=content_type_pk)
        # self.request.cart.add_item(self.request, from_date, to_date, quantity, content_type, object_id)
        return super(AddRoomsToCart, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_business_owner():
            return HttpResponseRedirect(reverse_lazy('business_profile'))
        return super(AddRoomsToCart, self).dispatch(request, *args, **kwargs)


add_rooms_to_cart = AddRoomsToCart.as_view()


class RoomPriceCategoriesListView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, PrefetchRelatedMixin, JsonMixin,
                                  DetailView):
    ajax_template_name = "hotels/includes/ajax_price_category_list.html"
    prefetch_related = ("price_categories",
                        "price_categories__prices",
                        "price_categories__translations",
                        "price_categories__type__translations",
                        "price_categories__meal_plan__translations")
    model = Room
    slug_field = "slug__iexact"
    tab_name = "service"

room_prices = RoomPriceCategoriesListView.as_view()


class RoomPriceCategoryCreateView(BusinessOwnerOnlyMixin, NamedFormsetsMixin, JsonMixin, CreateWithInlinesView):
    template_name = 'hotels/includes/ajax_price_category_edit.html'
    success_template_name = 'hotels/includes/ajax_price_category_view.html'
    inlines = [RoomPriceCategoryTranslationsInline,
               RoomPriceCategoryPricesInline]
    inlines_names = ['translations_formset',
                     'prices_formset']
    form_class = RoomPriceCategoryForm

    def get_template_names(self):
        if getattr(self, '_forms_valid', False):
            return [self.success_template_name]
        else:
            return super(RoomPriceCategoryCreateView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(RoomPriceCategoryCreateView, self).get_context_data(**kwargs)
        context['room'] = self._room
        context['form_prefix'] = self.get_prefix()
        context['create_view'] = True
        context['update_view'] = not context['create_view']
        return context

    def get_prefix(self):
        if hasattr(self, '_prefix'):
            return self._prefix
        else:
            if self.object:
                return super(RoomPriceCategoryCreateView, self).get_prefix()
            else:
                if self.request.method == "GET":
                    prefix = "t%d" % int(time.time())
                else:
                    prefix = self.request.POST['prefix']
            self._prefix = prefix
            return prefix

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)

        # save room explicitly
        self.object.item = self._room

        self.object.save()

        for formset in inlines:
            formset.save()

        # TODO: generate prices for every price category separately
        self.object.generate_price_ranges_according_to_default(self.object)

        self._forms_valid = True

        return self.render_to_response(self.get_context_data(price_category=self.object))

    def dispatch(self, request, *args, **kwargs):
        # TODO: ensure that only owner can access this page
        slug = kwargs.get('slug', None)
        try:
            room = Room.objects.get(slug__iexact=slug)
        except Room.DoesNotExist:
            raise Http404()
        else:
            self._room = room
        return super(RoomPriceCategoryCreateView, self).dispatch(request, *args, **kwargs)


room_price_category_create = RoomPriceCategoryCreateView.as_view()


class RoomPriceCategoryUpdateView(BusinessOwnerOnlyMixin, NamedFormsetsMixin, JsonMixin, UpdateWithInlinesView):
    template_name = 'hotels/includes/ajax_price_category_edit.html'
    inlines = [RoomPriceCategoryTranslationsInline, RoomPriceCategoryPricesInline]
    inlines_names = ['translations_formset', 'prices_formset']
    form_class = RoomPriceCategoryForm
    model = RoomPriceCategory

    def get_success_url(self):
        return reverse('room_price_category_view', kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(RoomPriceCategoryUpdateView, self).get_context_data(**kwargs)
        context['room'] = self.object.item
        context['form_prefix'] = self.get_prefix()
        context['create_view'] = False
        context['update_view'] = not context['create_view']
        return context

    def get_queryset(self):
        """
        Prices prefetching here is required cause formset uses it to display existing prices correctly (filtered and
                ordered).
        """
        return RoomPriceCategory.objects.prefetch_related(
            Prefetch('prices', queryset=RoomPrice.objects.filter(generated=False).order_by('from_date')))

    def get_prefix(self):
        prefix = "i%d" % self.object.id
        return prefix

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)

        self.object.save()

        for formset in inlines:
            formset.save()

        prices_changed = False
        for formset in inlines:
            if formset.has_changed():
                formset.save()
                # check if room prices formset has changed exactly
                if formset.model == RoomPrice:
                    prices_changed = True
        if prices_changed or 'regular_price' in form.changed_data:
            self.object.generate_price_ranges_according_to_default(self.object)

        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        # TODO: ensure that only owner can access this room price category
        return super(RoomPriceCategoryUpdateView, self).dispatch(request, *args, **kwargs)


room_price_category_update = RoomPriceCategoryUpdateView.as_view()


class RoomPriceCategoryDetailView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, DetailView):
    ajax_template_name = "hotels/includes/ajax_price_category_view.html"
    model = RoomPriceCategory
    tab_name = "service"
    context_object_name = "price_category"

    def get_context_data(self, **kwargs):
        context = super(RoomPriceCategoryDetailView, self).get_context_data(**kwargs)
        context['room'] = self.object.item
        return context

    def dispatch(self, request, *args, **kwargs):
        # TODO: ensure that only owner can access this room price category
        return super(RoomPriceCategoryDetailView, self).dispatch(request, *args, **kwargs)

room_price_category_view = RoomPriceCategoryDetailView.as_view()


class HotelGalleryImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "hotels/includes/ajax_hotel_gallery_image_crop.html"
    tab_name = "service"
    model = HotelImage
    form_class = HotelGalleryImageCropForm
    success_url = reverse_lazy('update_service')

    def form_valid(self, form):
        """
        It's required to explicitly change hotel status so that this changes will be visible and could be
        approved by admin.
        """
        self.object = form.save()
        if self.object.service.status == Hotel.UPDATING:
            self.object.service.status = Hotel.ON_MODERATION
            self.object.service.save()
        return super(HotelGalleryImageCropView, self).form_valid(form)

hotel_gallery_image_crop = HotelGalleryImageCropView.as_view()


class HotelFeaturedImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "hotels/includes/ajax_hotel_featured_image_crop.html"
    tab_name = "service"
    model = Hotel
    form_class = HotelFeaturedImageCropForm
    success_url = reverse_lazy('update_service')

    def form_valid(self, form):
        """
        It's required to explicitly change hotel status so that this changes will be visible and could be
        approved by admin.
        """
        self.object = form.save(commit=False)
        if self.object.status == Hotel.UPDATING:
            self.object.status = Hotel.ON_MODERATION
        self.object.save()
        return super(HotelFeaturedImageCropView, self).form_valid(form)


hotel_featured_image_crop = HotelFeaturedImageCropView.as_view()


class RoomImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "hotels/includes/ajax_room_image_crop.html"
    tab_name = "service"
    model = Room
    form_class = RoomImageCropForm

    def get_success_url(self):
        return reverse('update_item', kwargs={"slug": self.object.slug})

room_image_crop = RoomImageCropView.as_view()


class RoomPriceCategoryDeleteView(BusinessOwnerOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        data = {}

        price_category_pk = kwargs.get('pk', None)
        if price_category_pk:
            try:
                price_category = RoomPriceCategory.objects.get(pk=price_category_pk)
            except RoomPriceCategory.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no price category with this pk.'
            else:
                if price_category.item.service.owner != request.user:
                    data['status'] = 'fail'
                    data['message'] = 'There is no price category with this pk.'
                else:
                    price_category.delete()
                    data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect price category pk'

        return JsonResponse(data)

room_price_category_delete = RoomPriceCategoryDeleteView.as_view()


class RoomSpecialPriceDeleteView(BusinessOwnerOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        data = {}

        special_price_pk = kwargs.get('pk', None)
        if special_price_pk:
            try:
                special_price = RoomPrice.objects.get(generated=False, pk=special_price_pk)
            except RoomPrice.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no special price with this pk.'
            else:
                price_category = special_price.price_category
                if price_category.item.service.owner != request.user:
                    data['status'] = 'fail'
                    data['message'] = 'There is no special price with this pk.'
                else:
                    special_price.delete()
                    RoomPriceCategory.generate_price_ranges_according_to_default(price_category)
                    data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect special price pk'

        return JsonResponse(data)

room_special_price_delete = RoomSpecialPriceDeleteView.as_view()


class RemoveRoomView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):

        data = {}

        room_slug = kwargs.get('slug', None)
        if room_slug:
            try:
                room = request.user.get_original_service().items.get(slug__iexact=room_slug)
            except Room.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no room with this slug.'
            else:
                room.delete()
                data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect room slug'

        return JsonResponse(data)


remove_room = RemoveRoomView.as_view()


class RoomShowOnSiteAttrEditView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):

        data = {}

        room_slug = kwargs.get('slug', None)
        if room_slug:
            try:
                room = request.user.get_original_service().items.get(slug__iexact=room_slug)
            except Room.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no room with this slug.'
            else:
                show_on_site = request.POST.get('enable')
                new_val = True if show_on_site == "" else False
                if room.show_on_site != new_val:
                    room.show_on_site = new_val
                    room.save()
                data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect room slug'

        return JsonResponse(data)


room_show_on_site_attr_change = RoomShowOnSiteAttrEditView.as_view()


class RoomAllotmentAttrEditView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):

        data = {}

        new_val_str = request.POST.get("val")

        try:
            new_val = int(new_val_str)
        except ValueError:
            new_val = None

        if new_val is not None and new_val >= 0:
            room_slug = kwargs.get('slug', None)
            if room_slug:
                try:
                    room = request.user.get_original_service().items.get(slug__iexact=room_slug)
                except Room.DoesNotExist:
                    data['status'] = 'fail'
                    data['message'] = 'There is no room with this slug.'
                else:
                    if room.allotment != new_val:
                        room.allotment = new_val
                        room.save()
                    data['status'] = 'success'
            else:
                data['status'] = 'fail'
                data['message'] = 'Incorrect room slug'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect params'

        return JsonResponse(data)


room_allotment_attr_change = RoomAllotmentAttrEditView.as_view()


class NewHotelCommentView(EndUserOnlyMixin, AjaxNewServiceCommentMixin, View):
    form_class = HotelCommentForm
    model = HotelComment

new_hotel_comment = NewHotelCommentView.as_view()


class HotelCommentList(CommentList, View):
    ajax_template_name = "hotels/comment_list.html"
    model = HotelComment
    paginated_by = 20


comment_list = HotelCommentList.as_view()


class NewHotelReviewView(EndUserOnlyMixin, AjaxNewReviewMixin, View):
    ajax_template_name = "hotels/includes/ajax_review_block.html"
    service_model = Hotel
    review_model = HotelReview
    form_class = HotelReviewForm

new_hotel_review = NewHotelReviewView.as_view()
