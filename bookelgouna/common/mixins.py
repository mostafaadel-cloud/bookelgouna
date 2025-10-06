# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import get_language

from hotels.forms import HotelForm, HotelImageInline, RoomForm, HotelTranslationsInline, \
    RoomTranslationsInline
from transport.forms import TransportTranslationsInline, TransportImageInline, TransportForm, \
    TransportItemTranslationsInline, TransportItemImageInline, TransportItemForm, TransportItemDiscountInline
from apartments.forms import ApartmentForm, ApartmentTranslationsInline, ApartmentImageInline
from apartments.models import Apartment
from sports.forms import SportTranslationsInline, SportImageInline, SportForm, SportItemImageInline, \
    SportItemTranslationsInline, SportItemForm, SportItemDiscountInline
from excursions.forms import ExcursionImageInline, ExcursionTranslationsInline, ExcursionForm, \
    ExcursionItemTranslationsInline, ExcursionItemImageInline, ExcursionItemForm, ExcursionItemDiscountInline
from entertainment.forms import EntertainmentTranslationsInline, EntertainmentImageInline, EntertainmentForm, \
    EntertainmentItemTranslationsInline, EntertainmentItemImageInline, EntertainmentItemForm, \
    EntertainmentItemDiscountInline
from users.models import BusinessOwnerInfo

from .forms import TempImageForm, FeaturedImageForm, MultipleImagesForm, DatesAndGuestsForm
from .models import ModeratableModel, TempFile, ReservationPhoneSettings


class ServiceDependentServiceDataMixin(object):
    create_view = None

    def get_success_url(self):
        if self.user.is_apt_owner():
            return reverse('apt_prices', kwargs={"slug": self.object.slug})
        return reverse('items_list')

    def get_ajax_template_names(self):
        if self.user.is_hotel_owner():
            return ['hotels/includes/ajax_business_profile_tab_edit_hotel.html']
        elif self.user.is_apt_owner():
            return ['apartments/includes/ajax_business_profile_tab_edit_apt.html']
        elif self.user.is_transport_owner():
            return ['transport/includes/ajax_business_profile_tab_edit_transport.html']
        elif self.user.is_sports_owner():
            return ['sports/includes/ajax_business_profile_tab_edit_sport.html']
        elif self.user.is_excursions_owner():
            return ['excursions/includes/ajax_business_profile_tab_edit_excur.html']
        elif self.user.is_entertainment_owner():
            return ['entertainment/includes/ajax_business_profile_tab_edit_entert.html']

    def get_inlines(self):
        if self.user.is_hotel_owner():
            return [HotelImageInline, HotelTranslationsInline]
        elif self.user.is_apt_owner():
            return [ApartmentImageInline, ApartmentTranslationsInline]
        elif self.user.is_transport_owner():
            return [TransportImageInline, TransportTranslationsInline]
        elif self.user.is_sports_owner():
            return [SportImageInline, SportTranslationsInline]
        elif self.user.is_excursions_owner():
            return [ExcursionImageInline, ExcursionTranslationsInline]
        elif self.user.is_entertainment_owner():
            return [EntertainmentImageInline, EntertainmentTranslationsInline]

    def get_inlines_names(self):
        return ['images_formset', 'translations_formset']

    def get_form_class(self):
        if self.user.is_hotel_owner():
            return HotelForm
        elif self.user.is_apt_owner():
            return ApartmentForm
        elif self.user.is_transport_owner():
            return TransportForm
        elif self.user.is_sports_owner():
            return SportForm
        elif self.user.is_excursions_owner():
            return ExcursionForm
        elif self.user.is_entertainment_owner():
            return EntertainmentForm

    def get_object(self, queryset=None):
        services_manager = self.user.services_manager
        if self.user.is_apt_owner():
            if 'slug' not in self.kwargs:
                raise Http404
            else:
                slug = self.kwargs['slug']
                try:
                    apt = services_manager.get(slug__iexact=slug)
                except Apartment.DoesNotExist:
                    raise Http404
                else:
                    return apt
        # other services
        first = services_manager.first()
        if first.has_duplicate():
            duplicate = first.duplicate
        elif first.has_origin():
            duplicate = first
        else:
            if self.request.method == 'POST':
                raise NotImplementedError()
            duplicate = first.create_object_duplicate_from_given()
            duplicate.status = ModeratableModel.UPDATING
            duplicate.save()
        return duplicate

    def dispatch(self, request, *args, **kwargs):
        if self.create_view and (not self.user.is_apt_owner()):
            if request.user.has_service():
                return HttpResponseRedirect(reverse('items_list'))
        return super(ServiceDependentServiceDataMixin, self).dispatch(request, *args, **kwargs)

    @property
    def user(self):
        return self.request.user


class ServiceDependentItemDataMixin(object):
    create_view = None

    def get_ajax_template_names(self):
        if self.user.is_hotel_owner():
            return ['hotels/includes/ajax_business_profile_tab_edit_room.html']
        elif self.user.is_transport_owner():
            return ['transport/includes/ajax_business_profile_tab_edit_item.html']
        elif self.user.is_sports_owner():
            return ['sports/includes/ajax_business_profile_tab_edit_item.html']
        elif self.user.is_excursions_owner():
            return ['excursions/includes/ajax_business_profile_tab_edit_item.html']
        elif self.user.is_entertainment_owner():
            return ['entertainment/includes/ajax_business_profile_tab_edit_item.html']

    def construct_inlines(self):
        """
        Returns the inline formset instances
        """
        inline_formsets = []
        for inline_class in self.get_inlines():
            if self.request.method == 'POST':
                if not self.create_view:
                    if (self.user.is_transport_owner() and inline_class == TransportItemDiscountInline and
                            self.object.is_one_ride_item) or \
                        (self.user.is_sports_owner() and inline_class == SportItemDiscountInline and
                         self.object.is_one_time_item) or \
                        (self.user.is_excursions_owner() and inline_class == ExcursionItemDiscountInline and
                         self.object.is_one_time_item) or \
                        (self.user.is_entertainment_owner() and inline_class == EntertainmentItemDiscountInline and
                         self.object.is_one_time_item):
                        # skip discount prices inline if item is not time based
                        continue
            inline_instance = inline_class(self.model, self.request, self.object, self.kwargs, self)
            inline_formset = inline_instance.construct_formset()
            inline_formsets.append(inline_formset)
        return inline_formsets

    def get_inlines(self):
        if self.user.is_hotel_owner():
            return [RoomTranslationsInline]
        elif self.user.is_transport_owner():
            return [TransportItemImageInline, TransportItemTranslationsInline, TransportItemDiscountInline]
        elif self.user.is_sports_owner():
            return [SportItemImageInline, SportItemTranslationsInline, SportItemDiscountInline]
        elif self.user.is_excursions_owner():
            return [ExcursionItemImageInline, ExcursionItemTranslationsInline, ExcursionItemDiscountInline]
        elif self.user.is_entertainment_owner():
            return [EntertainmentItemImageInline, EntertainmentItemTranslationsInline, EntertainmentItemDiscountInline]

    def get_inlines_names(self):
        if self.user.is_hotel_owner():
            return ['translations_formset']
        return ['images_formset', 'translations_formset', 'discount_prices_formset']

    def get_queryset(self):
        return self.request.user.get_original_service().items.all()

    def get_form_class(self):
        if self.user.is_hotel_owner():
            return RoomForm
        elif self.user.is_transport_owner():
            return TransportItemForm
        elif self.user.is_sports_owner():
            return SportItemForm
        elif self.user.is_excursions_owner():
            return ExcursionItemForm
        elif self.user.is_entertainment_owner():
            return EntertainmentItemForm

    def dispatch(self, request, *args, **kwargs):
        if self.user.is_apt_owner():
            return HttpResponseRedirect(reverse('service_view'))
        return super(ServiceDependentItemDataMixin, self).dispatch(request, *args, **kwargs)

    @property
    def user(self):
        return self.request.user


class AjaxImagesUploadMixin(object):
    new_featured_image = None
    new_gallery_images = None

    def get_context_data(self, **kwargs):
        context = super(AjaxImagesUploadMixin, self).get_context_data(**kwargs)
        context['featured_image_form'] = FeaturedImageForm()
        context['multiple_images_form'] = MultipleImagesForm()
        if self.new_featured_image is not None:
            context['new_featured_image'] = self.new_featured_image
        if self.new_gallery_images is not None:
            context['new_gallery_images'] = self.new_gallery_images
        return context

    def forms_invalid(self, form, inlines):
        if 'featured_image_pk' not in form.errors:
            featured_image_pk = form.cleaned_data.get('featured_image_pk')
            if featured_image_pk:
                temp_file = TempFile.objects.get(pk=featured_image_pk)
                self.new_featured_image = temp_file

        if 'multiple_image_pk' not in form.errors:
            multiple_image_pk = form.cleaned_data.get('multiple_image_pk')
            if multiple_image_pk:
                temp_files = TempFile.objects.in_bulk(multiple_image_pk.split(','))
                self.new_gallery_images = temp_files
        return super(AjaxImagesUploadMixin, self).forms_invalid(form, inlines)


class SaveDatesAndGuestsInSessionMixin(object):
    def save_dates_and_guests(self, request, set_anyway=False, prefix=""):
        form = self.form_class(request.POST, prefix=prefix)
        if form.is_valid():
            fields = ['arrival', 'departure', 'adults', 'children']
            for field in fields:
                request.session[field] = form.cleaned_data[field]
            return True, []
        else:
            if set_anyway:
                for field_name, field_value in form.default_data().iteritems():
                    request.session[field_name] = field_value
            return False, [e for k, v in form.errors.items() for e in v]


class JsonMixin(object):
    extra_ajax_params = None

    def get_extra_ajax_params(self):
        return self.extra_ajax_params if self.extra_ajax_params is not None else {}

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            data = {
                'html': render_to_string(self.get_template_names(), context,
                                         context_instance=RequestContext(self.request)),
                'url': self.request.get_full_path()
            }

            data.update(self.get_extra_ajax_params())
            return JsonResponse(data, **response_kwargs)
        else:
            return super(JsonMixin, self).render_to_response(context, **response_kwargs)


class AjaxNewCommentMixin(object):
    ajax_template_name = None
    form_prefix = "comment"
    form_class = None
    model = None
    form_url = None

    def get_ajax_template_name(self):
        return self.ajax_template_name

    def get_form_class(self):
        return self.form_class

    def get_model(self):
        return self.model

    def get_form_prefix(self):
        return self.form_prefix

    def get_form_url(self):
        return reverse('new_{}'.format(self.get_model()._meta.model_name))

    def post(self, request, *args, **kwargs):
        data = {}

        form_class = self.get_form_class()
        form_prefix = self.get_form_prefix()
        form = form_class(request.POST, prefix=form_prefix, request=request)
        if form.is_valid():
            entity_id = form.cleaned_data['entity_id']
            model = self.get_model()
            model.objects.create(creator=request.user, text=form.cleaned_data['text'], entity_id=entity_id,
                                 language=get_language())
            data['status'] = 'success'
        else:
            data['status'] = 'fail'
            form_key = "{}_form".format(form_prefix)
            context = {
                form_key: form,
                'comment_url': self.get_form_url()
            }

            data['html'] = render_to_string(self.ajax_template_name, context, context_instance=RequestContext(request))
        return JsonResponse(data)


class AjaxNewServiceCommentMixin(AjaxNewCommentMixin):
    ajax_template_name = "common/includes/ajax_comment_form_block.html"


class CommentList(object):
    ajax_template_name = None
    model = None
    paginated_by = None

    def get_ajax_template_name(self):
        return self.ajax_template_name

    def get_model(self):
        return self.model

    def get_paginated_by(self):
        return self.paginated_by

    def get(self, request, *args, **kwargs):
        data = {
            'status': 'fail',
            'message': 'internal error has occurred'
        }

        next_page = request.GET.get("next_page", None)
        if next_page:
            next_page = int(next_page)
            entity_id = request.GET.get("entity_id", None)
            if entity_id:
                entity_id = int(entity_id)
                from_idx = self.get_paginated_by() * (next_page - 1)
                to_idx = self.get_paginated_by() * next_page
                model = self.get_model()
                comments = model.displayable.filter(entity_id=entity_id).select_related("creator")
                has_more_comments = comments.count() > to_idx
                context = {
                    "comments": comments[from_idx:to_idx],
                    "has_more_comments": has_more_comments,
                    "entity_id": entity_id,
                }
                if has_more_comments:
                    context["next_page"] = next_page + 1
                data['status'] = 'success'
                data['html'] = render_to_string(self.get_ajax_template_name(), context,
                                                context_instance=RequestContext(request)),

        return JsonResponse(data)


class AjaxNewReviewMixin(object):
    ajax_template_name = None
    service_model = None
    review_model = None
    form_class = None

    def post(self, request, *args, **kwargs):

        data = {}

        rate_str = request.POST.get('rate')
        service_pk = request.POST.get('pk')

        if rate_str is not None:
            try:
                rate = int(rate_str)
            except ValueError:
                rate = None
            if rate and service_pk:
                try:
                    service = self.service_model.originals.get(pk=service_pk)
                except self.service_model.DoesNotExist:
                    # this is required to filter out duplicate services rating
                    pass
                else:
                    form_data = {
                        'rate': rate,
                        'service': service_pk,
                        'reviewer': request.user.pk
                    }
                    form = self.form_class(data=form_data)
                    if form.is_valid():
                        form.save()
                        service.recalculate_review_avg(rate)
                        context = {
                            'can_review': False,
                            'service': service,
                            'user_review': rate,
                        }
                        data['status'] = 'success'
                        data['html'] = render_to_string(self.ajax_template_name, context,
                                                        context_instance=RequestContext(request))
        if 'status' not in data:
            data['status'] = 'fail'
            data['message'] = 'Incorrect params'

        return JsonResponse(data)


class UploadImagesMixin(object):
    images_key = None

    def post(self, request, *args, **kwargs):
        data = {}
        valid_images = []
        invalid_images = []
        for image in request.FILES.getlist(self.images_key):
            form = TempImageForm(files={'image': image})
            if form.is_valid():
                img = form.save()
                valid_images.append({'pk': img.pk, 'url': img.business_owner_page_thumbnail()})
            else:
                if 'image' in form.errors:
                    error = form.errors['image']
                    invalid_images.append(image.name + ": " + error)
        data['status'] = 'success'
        data['valid'] = valid_images
        data['invalid'] = invalid_images
        return JsonResponse(data)


class SetDatesAndGuestsIntoSessionMixin(object):
    def dispatch(self, request, *args, **kwargs):
        required_keys = ['arrival', 'departure', 'adults', 'children']
        if not all([key in request.session for key in required_keys]):
            for field_name, field_value in DatesAndGuestsForm.default_data().iteritems():
                request.session[field_name] = field_value
        return super(SetDatesAndGuestsIntoSessionMixin, self).dispatch(request, *args, **kwargs)


class ReservationPhoneToContextMixin(object):
    business_type = None

    def get_context_data(self, **kwargs):
        context = super(ReservationPhoneToContextMixin, self).get_context_data(**kwargs)
        if self.business_type is None or self.business_type not in dict(BusinessOwnerInfo.SERVICE_TYPES):
            raise ImproperlyConfigured('Mixin user must define "business_type" with value from '
                                       'BusinessOwnerInfo.SERVICE_TYPES choices.')
        s = ReservationPhoneSettings.objects.filter(enabled_for_services__contains=self.business_type,
                                                    is_enabled=True).first()
        if s is not None:
            context['reservation_phone'] = s.phone
        return context
