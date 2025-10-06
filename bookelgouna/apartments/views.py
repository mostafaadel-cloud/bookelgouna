from aggregate_if import Min, Max, Sum
from braces.views import PrefetchRelatedMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import pgettext_lazy
from extra_views import CreateWithInlinesView, NamedFormsetsMixin, UpdateWithInlinesView
from skd_tools.mixins import ActiveTabMixin
import time

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Prefetch
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.utils.functional import cached_property
from django.views.generic import DetailView, FormView, View, UpdateView
from django.views.generic.edit import FormMixin
from booking.utils import get_order_item_with_this_item_in_dates

from common.mixins import CommentList, JsonMixin, AjaxNewReviewMixin, \
    SetDatesAndGuestsIntoSessionMixin, AjaxNewServiceCommentMixin, ReservationPhoneToContextMixin
from common.utils import get_arrival_from_session_or_default, get_departure_from_session_or_default
from users.mixins import BusinessOwnerOnlyMixin, EndUserOnlyMixin, BusinessProfileTabMixin
from users.models import BusinessOwnerInfo

from .forms import ApartmentCommentForm, ApartmentSearchForm, CartItemForm, PriceSearchForm, \
    AptPriceCategoryTranslationsInline, AptPriceCategoryForm, AptPriceCategoryPricesInline, AptFeaturedImageCropForm, \
    AptGalleryImageCropForm, ApartmentReviewForm, ApartmentOptionsForm
from .models import ApartmentComment, Apartment, ApartmentPriceCategory, ApartmentReview, ApartmentPrice, ApartmentImage


class ApartmentDetailView(SetDatesAndGuestsIntoSessionMixin, ReservationPhoneToContextMixin, ActiveTabMixin,
                          DetailView):
    active_tab = 'apartment'
    template_name = 'apartments/apartment_detail.html'
    ajax_template_name = 'apartments/includes/ajax_apartment_detail.html'
    queryset = Apartment.objects.prefetch_related('images', 'translations', 'price_category__translations',
                                                  'amenities__translations')
    comments_paginated_by = 10
    slug_field = 'slug__iexact'
    context_object_name = 'apartment'
    business_type = BusinessOwnerInfo.APARTMENT

    def get_object(self, queryset=None):
        if not hasattr(self, '_object'):
            self._object = super(ApartmentDetailView, self).get_object(queryset)
        return self._object

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super(ApartmentDetailView, self).get_context_data(**kwargs)

        if 'detail-arrival' in self.request.GET or 'detail-departure' in self.request.GET:
            # there are some values for these fields so we should examine them
            form = PriceSearchForm(data=self.request.GET, prefix='detail')
            if form.is_valid():
                from_date = form.cleaned_data['arrival']
                to_date = form.cleaned_data['departure']
            else:
                context['errors'] = [e for k, v in form.errors.items() for e in v]
                context['dates_form'] = form
        else:
            from_date = get_arrival_from_session_or_default(self.request)
            to_date = get_departure_from_session_or_default(self.request)

        price_category = self.object.get_price_category()
        apt_options = self.object.get_options()
        context['has_price_category'] = price_category is not None
        context['has_enabled_options'] = apt_options is not None and (apt_options.for_long_term or apt_options.for_sale)
        context['apt_options'] = apt_options
        if 'errors' not in context:
            context['price_category'] = price_category
            if price_category:
                context['in_cart'] = self.request.cart.in_cart(context['price_category'])
                context['in_order'] = get_order_item_with_this_item_in_dates(context['price_category'],
                                                                             from_date, to_date)
            context['start_date'] = from_date
            context['end_date'] = to_date

        if 'dates_form' not in context:
            initial = {
                'arrival': from_date,
                'departure': to_date,
            }
            context['dates_form'] = PriceSearchForm(prefix='detail', initial=initial)
            initial_cartitem = {
                'from_date': from_date,
                'to_date': to_date,
                'item_pk': self.object.pk
            }
            context['cartitem_form'] = CartItemForm(prefix='cartitem', initial=initial_cartitem)
            context['night_number'] = (to_date - from_date).days
        comments = ApartmentComment.displayable.filter(entity_id=self.object.pk).select_related("creator")
        context['comments'] = comments[:self.comments_paginated_by]
        context['has_more_comments'] = comments.count() > self.comments_paginated_by
        context['can_add_comment'] = False
        context['can_review'] = False
        user = self.request.user
        if user.is_authenticated() and user.is_end_user() and not user.is_staff:
            has_comments_to_this_apartment = self.request.user.apartment_comments.filter(entity_id=self.object.pk).exists()
            context['can_add_comment'] = not has_comments_to_this_apartment
            apartment_review = self.request.user.apartment_reviews.filter(service_id=self.object.pk).first()
            context['show_rate_block'] = True
            context['can_review'] = not apartment_review
            if apartment_review:
                context['user_review'] = apartment_review.rate
        elif not user.is_authenticated():
            context['can_add_comment'] = True
            context['login_url'] = '{}?next={}?scroll=1'.format(reverse('account_login'), self.request.path)
        if context['can_add_comment']:
            initial_comment_form = {
                'entity_id': self.object.pk,
            }
            context['comment_form'] = ApartmentCommentForm(prefix='comment', initial=initial_comment_form)
        return context

    def get_adults_from_session_or_default(self):
        return self.request.session.get('adults', 0)

    def get_children_from_session_or_default(self):
        return self.request.session.get('children', 0)

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        apartment = self.get_object()
        staff_or_real_owner = user.is_authenticated() and (user.is_staff or (user.is_business_owner() and
                                                                             apartment.owner == user))
        if staff_or_real_owner:
            if not request.is_ajax() and apartment.status != Apartment.APPROVED:
                messages.warning(request,
                                 pgettext_lazy('apartment detail page not approved service warning message',
                                               'This apartment is not approved and can be viewed by you only.'))
        else:
            if not (apartment.is_origin() and apartment.status == Apartment.APPROVED and apartment.show_on_site and
                        (apartment.has_prices() or apartment.review_mode)):
                raise Http404()
        return super(ApartmentDetailView, self).dispatch(request, *args, **kwargs)


view_apartment = ApartmentDetailView.as_view()


class ApartmentListView(SetDatesAndGuestsIntoSessionMixin, ActiveTabMixin, FormView):
    active_tab = 'apartment'
    form_class = ApartmentSearchForm
    template_name = 'apartments/find_apartment.html'
    ajax_list_only_template_name = 'apartments/includes/ajax_find_apartment_list_only.html'
    ajax_list_with_filters_template_name = 'apartments/includes/ajax_find_apartment_list_with_filters.html'
    paginated_by = 10

    def get_initial(self):
        initial = super(ApartmentListView, self).get_initial()
        initial.update({
            'from_price': self.get_from_price(),
            'to_price': self.get_to_price(),
            'room_num_from': self.room_num_from,
            'room_num_to': self.room_num_to,
            'type': self.type,
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
        context = super(ApartmentListView, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        from_date = self.get_from_date()
        to_date = self.get_to_date()
        context['apartment_to_order_item'] = {
            a.pk: get_order_item_with_this_item_in_dates(a.get_price_category(), from_date, to_date)
            for a in context['object_list'] if a.get_price_category() is not None}
        context['min_price'] = self.get_min_price()
        context['max_price'] = self.get_max_price()
        context['room_num_min'] = self.get_room_num_min()
        context['room_num_max'] = self.get_room_num_max()
        context['night_number'] = (self.get_to_date() - self.get_from_date()).days
        context['has_more_apartments'] = self.has_more_apartments
        return context

    @cached_property
    def room_num(self):
        room_num_range = Apartment.originals.aggregate(min=Min('number_of_rooms'), max=Max('number_of_rooms'))
        if room_num_range['min'] and room_num_range['min'] == room_num_range['max']:
            room_num_range['max'] += 1
        return room_num_range

    def get_room_num_min(self):
        return self.room_num['min']

    def get_room_num_max(self):
        return self.room_num['max']

    @cached_property
    def room_num_from(self):
        v = None
        if 'room_num_from' in self.request.GET:
            try:
                v = float(self.request.GET['room_num_from'])
            except ValueError:
                pass
        if v is None:
            v = self.get_room_num_min()
        return v

    @cached_property
    def room_num_to(self):
        v = None
        if 'room_num_to' in self.request.GET:
            try:
                v = float(self.request.GET['room_num_to'])
            except ValueError:
                pass
        if v is None:
            v = self.get_room_num_max()
        return v

    @cached_property
    def type(self):
        return self.request.GET.getlist('type', [c[0] for c in Apartment.TYPES])

    def get_queryset(self):
        if self.room_num_from and self.room_num_to and self.get_from_price() and self.get_to_price():
            q = Apartment.originals.filter(type__in=self.type, number_of_rooms__gte=self.room_num_from,
                                           number_of_rooms__lte=self.room_num_to)
            first_day = self.get_from_date()
            q = q.annotate(price_per_night=Min('price_category__prices__price',
                           only=(Q(price_category__prices__isnull=False) &
                                 Q(price_category__prices__from_date__lte=first_day) &
                                 Q(price_category__prices__to_date__gt=first_day))))

            if self.get_min_price() != self.get_from_price() or self.get_max_price() != self.get_to_price():
                q = q.filter(Q(price_per_night__gte=self.from_price) & Q(price_per_night__lte=self.to_price) |
                             (Q(price_per_night=True) & Q(review_mode=True)))
            q = q.order_by('price_per_night')
            from_index = self.paginated_by * (self.get_page() - 1)
            to_index = self.paginated_by * self.get_page()
            self.has_more_apartments = q.count() > to_index
            q = q[from_index:to_index].prefetch_related('translations', 'images')
        else:
            q = []
            self.has_more_apartments = False
        return q

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
        price_range = ApartmentPrice.objects.filter(
                           Q(from_date__lte=self.get_from_date(), to_date__gte=self.get_from_date()) |
                           Q(from_date__lte=self.get_to_date(), to_date__gte=self.get_to_date()) |
                           Q(from_date__lte=self.get_from_date(), to_date__gte=self.get_to_date()) |
                           Q(from_date__gte=self.get_from_date(), to_date__lte=self.get_to_date())).aggregate(min=Min('price'), max=Max('price'))

        if price_range['min'] and price_range['min'] == price_range['max']:
            price_range['max'] += 1

        if not price_range['min']:
            price_range = ApartmentPriceCategory.objects.aggregate(min=Min('regular_price'), max=Max('regular_price'))

            if price_range['min'] and price_range['min'] == price_range['max']:
                price_range['max'] += 1

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


find_apartment = ApartmentListView.as_view()


class AddApartmentToCart(FormView):
    form_class = CartItemForm
    success_url = reverse_lazy('cart')
    prefix = 'cartitem'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('find_apartment'))

    def form_invalid(self, form):
        if 'HTTP_REFERER' in self.request.META:
            failure_url = self.request.META['HTTP_REFERER']
        else:
            failure_url = reverse_lazy('explore')
        return HttpResponseRedirect(failure_url)

    def form_valid(self, form):
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']
        item_pk = form.cleaned_data['item_pk']
        if item_pk:
            try:
                item = Apartment.objects.get(price_category__isnull=False, pk=item_pk)
            except Apartment.DoesNotExist:
                pass
            else:
                if item.is_origin() and item.show_on_site:
                    price_category = item.get_price_category()
                    if price_category is not None:
                        # prevent from book apartment that is already booked on selected dates
                        if get_order_item_with_this_item_in_dates(price_category, from_date, to_date) is None:
                            content_type = ContentType.objects.get_for_model(ApartmentPriceCategory)
                            self.request.cart.add_item(self.request, from_date, to_date, 1, content_type, price_category.pk)
        return super(AddApartmentToCart, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_business_owner():
            return HttpResponseRedirect(reverse_lazy('business_profile'))
        return super(AddApartmentToCart, self).dispatch(request, *args, **kwargs)


add_apartment_to_cart = AddApartmentToCart.as_view()


class AptPriceCategoriesListView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, PrefetchRelatedMixin, JsonMixin,
                                 DetailView):
    ajax_template_name = "apartments/includes/ajax_price_category_list.html"
    prefetch_related = ("price_category__prices", "price_category__translations")
    model = Apartment
    slug_field = "slug__iexact"
    context_object_name = "apartment"
    tab_name = "service"

    def get_context_data(self, **kwargs):
        context = super(AptPriceCategoriesListView, self).get_context_data(**kwargs)
        context['price_category'] = self.object.get_price_category()
        context['form'] = ApartmentOptionsForm(instance=self.object.get_options())
        return context


apt_prices = AptPriceCategoriesListView.as_view()


class AptOptionsFormView(BusinessOwnerOnlyMixin, JsonMixin, FormMixin, DetailView):
    template_name = 'apartments/includes/ajax_apt_options_form.html'
    model = Apartment
    slug_field = "slug__iexact"
    context_object_name = "apartment"
    form_class = ApartmentOptionsForm

    def get_form_kwargs(self):
        kwargs = super(AptOptionsFormView, self).get_form_kwargs()
        kwargs['instance'] = self.object.get_options()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AptOptionsFormView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.options = form.save(commit=False)
        self.options.service = self.object.get_original()
        self.options.save()
        messages.success(self.request, pgettext_lazy('business owner apartment options success message',
                                                     u'Apartment options were successfully updated.'))
        return self.render_to_response(self.get_context_data(form=form))

apt_options_view = AptOptionsFormView.as_view()


class AptPriceCategoryCreateView(BusinessOwnerOnlyMixin, NamedFormsetsMixin, JsonMixin, CreateWithInlinesView):
    template_name = 'apartments/includes/ajax_price_category_edit.html'
    success_template_name = 'apartments/includes/ajax_price_category_view.html'
    inlines = [AptPriceCategoryTranslationsInline,
               AptPriceCategoryPricesInline]
    inlines_names = ['translations_formset',
                     'prices_formset']
    form_class = AptPriceCategoryForm

    def get_template_names(self):
        if getattr(self, '_forms_valid', False):
            return [self.success_template_name]
        else:
            return super(AptPriceCategoryCreateView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(AptPriceCategoryCreateView, self).get_context_data(**kwargs)
        context['apartment'] = self._apartment
        context['form_prefix'] = self.get_prefix()
        context['create_view'] = True
        context['update_view'] = not context['create_view']
        return context

    def get_prefix(self):
        if hasattr(self, '_prefix'):
            return self._prefix
        else:
            if self.object:
                return super(AptPriceCategoryCreateView, self).get_prefix()
            else:
                if self.request.method == "GET":
                    prefix = "t%d" % int(time.time())
                else:
                    prefix = self.request.POST['prefix']
            self._prefix = prefix
            return prefix

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)
        self.object.item = self._apartment
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
            apartment = Apartment.objects.get(slug__iexact=slug)
        except Apartment.DoesNotExist:
            raise Http404()
        else:
            if apartment.is_duplicate():
                apartment = apartment.origin
            self._apartment = apartment
        return super(AptPriceCategoryCreateView, self).dispatch(request, *args, **kwargs)


apt_price_category_create = AptPriceCategoryCreateView.as_view()


class AptPriceCategoryUpdateView(BusinessOwnerOnlyMixin, NamedFormsetsMixin, JsonMixin, UpdateWithInlinesView):
    template_name = 'apartments/includes/ajax_price_category_edit.html'
    inlines = [AptPriceCategoryTranslationsInline, AptPriceCategoryPricesInline]
    inlines_names = ['translations_formset', 'prices_formset']
    form_class = AptPriceCategoryForm
    model = ApartmentPriceCategory

    def get_success_url(self):
        return reverse('apt_price_category_view', kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(AptPriceCategoryUpdateView, self).get_context_data(**kwargs)
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
        return ApartmentPriceCategory.objects.prefetch_related(
            Prefetch('prices', queryset=ApartmentPrice.objects.filter(generated=False).order_by('from_date')))

    def get_prefix(self):
        prefix = "i%d" % self.object.id
        return prefix

    def forms_valid(self, form, inlines):
        self.object = form.save()

        for formset in inlines:
            formset.save()

        prices_changed = False
        for formset in inlines:
            if formset.has_changed():
                formset.save()
                # check if room prices formset has changed exactly
                if formset.model == ApartmentPrice:
                    prices_changed = True
        if prices_changed or 'regular_price' in form.changed_data:
            self.object.generate_price_ranges_according_to_default(self.object)

        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        # TODO: ensure that only owner can access this room price category
        return super(AptPriceCategoryUpdateView, self).dispatch(request, *args, **kwargs)


apt_price_category_update = AptPriceCategoryUpdateView.as_view()


class AptPriceCategoryDetailView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, DetailView):
    ajax_template_name = "apartments/includes/ajax_price_category_view.html"
    model = ApartmentPriceCategory
    tab_name = "service"
    context_object_name = "price_category"

    def get_context_data(self, **kwargs):
        context = super(AptPriceCategoryDetailView, self).get_context_data(**kwargs)
        context['apartment'] = self.object.item
        return context

    def dispatch(self, request, *args, **kwargs):
        # TODO: ensure that only owner can access this room price category
        return super(AptPriceCategoryDetailView, self).dispatch(request, *args, **kwargs)

apt_price_category_view = AptPriceCategoryDetailView.as_view()


class ApartmentGalleryImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "apartments/includes/ajax_apartment_gallery_image_crop.html"
    tab_name = "service"
    model = ApartmentImage
    form_class = AptGalleryImageCropForm

    def get_success_url(self):
        return reverse('update_service_with_slug', args=(self.object.service.slug,))

    def get_context_data(self, **kwargs):
        context = super(ApartmentGalleryImageCropView, self).get_context_data(**kwargs)
        context['apartment'] = self.object.service
        return context

    def form_valid(self, form):
        """
        It's required to explicitly change apartment status so that this changes will be visible and could be
        approved by admin.
        """
        self.object = form.save()
        service = self.object.service
        if service.status == Apartment.UPDATING:
            service.status = Apartment.ON_MODERATION
            service.save()
        return super(ApartmentGalleryImageCropView, self).form_valid(form)

apt_gallery_image_crop = ApartmentGalleryImageCropView.as_view()


class AptFeaturedImageCropView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, UpdateView):
    ajax_template_name = "apartments/includes/ajax_apartment_featured_image_crop.html"
    tab_name = "service"
    model = Apartment
    form_class = AptFeaturedImageCropForm

    def get_success_url(self):
        return reverse('update_service_with_slug', args=(self.object.slug,))

    def form_valid(self, form):
        """
        It's required to explicitly change apartment status so that this changes will be visible and could be
        approved by admin.
        """
        self.object = form.save(commit=False)
        if self.object.status == Apartment.UPDATING:
            self.object.status = Apartment.ON_MODERATION
        self.object.save()
        return super(AptFeaturedImageCropView, self).form_valid(form)


apt_featured_image_crop = AptFeaturedImageCropView.as_view()


class AptPriceCategoryDeleteView(BusinessOwnerOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        data = {}

        price_category_pk = kwargs.get('pk', None)
        if price_category_pk:
            try:
                price_category = ApartmentPriceCategory.objects.get(pk=price_category_pk)
            except ApartmentPriceCategory.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no price category with this pk.'
            else:
                if price_category.item.owner != request.user:
                    data['status'] = 'fail'
                    data['message'] = 'There is no price category with this pk.'
                else:
                    price_category.delete()
                    data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect price category pk'

        return JsonResponse(data)

apt_price_category_delete = AptPriceCategoryDeleteView.as_view()


class AptSpecialPriceDeleteView(BusinessOwnerOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        data = {}

        special_price_pk = kwargs.get('pk', None)
        if special_price_pk:
            try:
                special_price = ApartmentPrice.objects.get(generated=False, pk=special_price_pk)
            except ApartmentPrice.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no special price with this pk.'
            else:
                price_category = special_price.price_category
                if price_category.item.owner != request.user:
                    data['status'] = 'fail'
                    data['message'] = 'There is no special price with this pk.'
                else:
                    special_price.delete()
                    ApartmentPriceCategory.generate_price_ranges_according_to_default(price_category)
                    data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect special price pk'

        return JsonResponse(data)

apt_special_price_delete = AptSpecialPriceDeleteView.as_view()

# DISABLED
# class RemoveAptView(BusinessOwnerOnlyMixin, View):
#
#     def post(self, request, *args, **kwargs):
#
#         data = {}
#
#         apt_slug = kwargs.get('slug', None)
#         if apt_slug:
#             try:
#                 # get duplicate
#                 apt = request.user.apartments.filter(origin__isnull=False).get(slug__iexact=apt_slug)
#             except ApartmentPriceCategory.DoesNotExist:
#                 data['status'] = 'fail'
#                 data['message'] = 'There is no apt with this slug.'
#             else:
#                 # remove its related origin
#                 apt.origin.delete()
#                 data['status'] = 'success'
#         else:
#             data['status'] = 'fail'
#             data['message'] = 'Incorrect apt slug'
#
#         return JsonResponse(data)
#
#
# remove_apt = RemoveAptView.as_view()


class AptShowOnSiteAttrEditView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):

        data = {}

        apt_slug = kwargs.get('slug', None)
        if apt_slug:
            try:
                apt = request.user.apartments.filter(origin__isnull=False).get(slug__iexact=apt_slug)
            except Apartment.DoesNotExist:
                data['status'] = 'fail'
                data['message'] = 'There is no apartment with this slug.'
            else:
                show_on_site = request.POST.get('enable')
                new_val = True if show_on_site == "" else False
                if apt.show_on_site != new_val:
                    apt.show_on_site = new_val
                    apt.save()
                    origin = apt.origin
                    origin.show_on_site = new_val
                    origin.save()
                data['status'] = 'success'
        else:
            data['status'] = 'fail'
            data['message'] = 'Incorrect apartment slug'

        return JsonResponse(data)


apt_show_on_site_attr_change = AptShowOnSiteAttrEditView.as_view()


class NewApartmentCommentView(EndUserOnlyMixin, AjaxNewServiceCommentMixin, View):
    form_class = ApartmentCommentForm
    model = ApartmentComment

new_apartment_comment = NewApartmentCommentView.as_view()


class ApartmentCommentList(CommentList, View):
    ajax_template_name = "apartments/comment_list.html"
    model = ApartmentComment
    paginated_by = 20


comment_list = ApartmentCommentList.as_view()


class NewApartmentReviewView(EndUserOnlyMixin, AjaxNewReviewMixin, View):
    ajax_template_name = "apartments/includes/ajax_review_block.html"
    service_model = Apartment
    review_model = ApartmentReview
    form_class = ApartmentReviewForm

new_apartment_review = NewApartmentReviewView.as_view()
