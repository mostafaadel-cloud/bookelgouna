import json

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, NamedFormsetsMixin

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.http import HttpResponse
from django.views.generic import View, ListView, TemplateView

from users.mixins import BusinessOwnerOnlyMixin, BusinessProfileTabMixin

from .forms import DatesAndGuestsPostForm, DatesAndGuestsAjaxForm, TempImageForm, MultipleImagesForm, FeaturedImageForm
from .mixins import ServiceDependentServiceDataMixin, ServiceDependentItemDataMixin, SaveDatesAndGuestsInSessionMixin, \
    JsonMixin, UploadImagesMixin, AjaxImagesUploadMixin
from .models import ModeratableModel, TempFile


class CreateService(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, ServiceDependentServiceDataMixin,
                    NamedFormsetsMixin, AjaxImagesUploadMixin, JsonMixin, CreateWithInlinesView):
    tab_name = 'service'
    create_view = True

    def get_context_data(self, **kwargs):
        context = super(CreateService, self).get_context_data(**kwargs)
        context['create_view'] = self.create_view
        return context

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)

        # save owner explicitly
        self.object.owner = self.request.user
        self.object.save()
        form.save_m2m()

        for formset in inlines:
            formset.save()

        self.object.generate_slug(commit=True)

        form.save_featured_image(create_view=self.create_view)
        form.save_multiple_images()

        # create duplicate
        self.object.create_object_duplicate_from_given()

        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        if self.user.is_authenticated() and self.user.is_business_owner():
            self.user.hide_next_link()
        return super(CreateService, self).dispatch(request, *args, **kwargs)


create_service = CreateService.as_view()


class UpdateService(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, ServiceDependentServiceDataMixin,
                    NamedFormsetsMixin, AjaxImagesUploadMixin, JsonMixin, UpdateWithInlinesView):
    tab_name = 'service'
    create_view = False
    success_url = reverse_lazy('items_list')

    def get_context_data(self, **kwargs):
        context = super(UpdateService, self).get_context_data(**kwargs)
        context['create_view'] = self.create_view
        return context

    def forms_valid(self, form, inlines):
        self.object = form.save()
        form.save_m2m()
        for formset in inlines:
            if formset.has_changed():
                formset.save()
        changed_featured_image = form.save_featured_image(create_view=self.create_view)
        new_multiple_images = form.save_multiple_images()
        form_changed_data_copy = list(form.changed_data)
        if 'featured_image_pk' in form_changed_data_copy:
            form_changed_data_copy.remove('featured_image_pk')
        if 'multiple_image_pk' in form_changed_data_copy:
            form_changed_data_copy.remove('multiple_image_pk')
        if self.user.is_apt_owner() and 'show_on_site' in form_changed_data_copy:
            form_changed_data_copy.remove('show_on_site')
            # change origin value also
            origin = self.object.origin
            origin.show_on_site = self.object.show_on_site
            origin.save()

        new_changes_to_approve = len(form_changed_data_copy) > 0 or any(formset.has_changed() for formset in inlines) \
                                 or changed_featured_image or new_multiple_images
        # Service requires moderation if only any of these 4 items is true:
        # 1. form data was changed (except images fields and show_on_site field for apartment)
        # 2. formset data was changed
        # 3. featured image was changed
        # 4. new multiple images were added
        if new_changes_to_approve and self.object.status == ModeratableModel.UPDATING:
            self.object.status = ModeratableModel.ON_MODERATION
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(UpdateService, self).dispatch(request, *args, **kwargs)
        except NotImplementedError:
            return HttpResponseRedirect(reverse_lazy('not_implemented'))


update_service = UpdateService.as_view()


class CreateItem(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, ServiceDependentItemDataMixin, NamedFormsetsMixin,
                 AjaxImagesUploadMixin, JsonMixin, CreateWithInlinesView):
    tab_name = 'service'
    create_view = True

    def get_success_url(self):
        if self.user.is_hotel_owner():
            return reverse('room_prices', kwargs={"slug": self.object.slug})
        return reverse('items_list')

    def get_context_data(self, **kwargs):
        context = super(CreateItem, self).get_context_data(**kwargs)
        context['create_view'] = self.create_view
        context['service'] = self.request.user.get_original_service()
        return context

    def forms_valid(self, form, inlines):
        self.object = form.save(commit=False)

        # save service explicitly
        self.object.service = self.request.user.get_original_service()
        self.object.save()
        form.save_m2m()

        for formset in inlines:
            formset.save()

        self.object.generate_slug(commit=True)

        form.save_featured_image(create_view=self.create_view)

        if not self.user.is_hotel_owner():
            form.save_multiple_images()

        return HttpResponseRedirect(self.get_success_url())

create_item = CreateItem.as_view()


class UpdateItem(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, ServiceDependentItemDataMixin, NamedFormsetsMixin,
                 AjaxImagesUploadMixin, JsonMixin, UpdateWithInlinesView):
    tab_name = 'service'
    create_view = False
    success_url = reverse_lazy('items_list')
    slug_field = "slug__iexact"

    def get_context_data(self, **kwargs):
        context = super(UpdateItem, self).get_context_data(**kwargs)
        context['create_view'] = self.create_view
        context['service'] = self.request.user.get_original_service()
        return context

    def get_queryset(self):
        return self.request.user.get_original_service().items.all()

    def get_object(self, queryset=None):
        item = super(UpdateItem, self).get_object()
        if item.service.owner != self.request.user:
            raise Http404()
        return item

    def forms_valid(self, form, inlines):
        self.object = form.save()
        form.save_m2m()

        for formset in inlines:
            if formset.has_changed():
                formset.save()

        form.save_featured_image(create_view=self.create_view)

        if not self.user.is_hotel_owner():
            form.save_multiple_images()

        return HttpResponseRedirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(UpdateItem, self).dispatch(request, *args, **kwargs)
        except NotImplementedError:
            return HttpResponseRedirect(reverse_lazy('not_implemented'))


update_item = UpdateItem.as_view()


class ItemsList(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, ListView):
    tab_name = "service"

    def get_ajax_template_names(self):
        if self.user.is_hotel_owner():
            return ['hotels/includes/ajax_business_profile_tab_room_list.html']
        elif self.user.is_apt_owner():
            return ['apartments/includes/ajax_business_profile_tab_apt_list.html']
        elif self.user.is_transport_owner():
            return ['transport/includes/ajax_business_profile_tab_item_list.html']
        elif self.user.is_sports_owner():
            return ['sports/includes/ajax_business_profile_tab_item_list.html']
        elif self.user.is_excursions_owner():
            return ['excursions/includes/ajax_business_profile_tab_item_list.html']
        elif self.user.is_entertainment_owner():
            return ['entertainment/includes/ajax_business_profile_tab_item_list.html']

    def get_queryset(self):
        if self.user.is_apt_owner():
            # three combinations are possible here:
            # 1. origin without duplicate [origin__isnull=True, duplicate__isnull=True],
            # 2. origin with duplicate [origin__isnull=True, duplicate__isnull=False],
            # 3. duplicate [origin__isnull=False, duplicate__isnull=True]
            # at first we should create duplicates for all origins without duplicates (1)
            for origin in self.request.user.apartments.filter(origin__isnull=True, duplicate__isnull=True):
                duplicate = origin.create_object_duplicate_from_given()
                duplicate.status = ModeratableModel.UPDATING
                duplicate.save()
            # then we should list duplicates only (3)
            return self.request.user.apartments.filter(origin__isnull=False, duplicate__isnull=True)\
                .prefetch_related('translations')
        else:
            return self.request.user.get_original_service().items.all()

    def get_context_data(self, **kwargs):
        context = super(ItemsList, self).get_context_data(**kwargs)
        if not self.user.is_apt_owner():
            context['service'] = original = self.request.user.get_original_service()
            duplicate = original.duplicate
            if duplicate is not None and duplicate.status != ModeratableModel.UPDATING:
                context['duplicate'] = original.duplicate
        return context

    @property
    def user(self):
        return self.request.user


items_list = ItemsList.as_view()


class NotImplementedView(BusinessOwnerOnlyMixin, BusinessProfileTabMixin, JsonMixin, TemplateView):
    tab_name = "service"

    def get_ajax_template_names(self):
        return ['common/includes/ajax_business_profile_tab_service_not_implemented.html']

not_implemented = NotImplementedView.as_view()


class SaveDatesAndGuestsAjaxView(SaveDatesAndGuestsInSessionMixin, View):
    form_class = DatesAndGuestsAjaxForm

    def post(self, request, *args, **kwargs):
        result = {}
        status, errors = self.save_dates_and_guests(request)
        if status:
            result['status'] = 'success'
        else:
            result['status'] = 'fail'
            result['errors'] = errors
            if 'arrival' in request.session:
                result['arrival'] = request.session['arrival'].strftime('%d.%m.%Y')
                result['departure'] = request.session['departure'].strftime('%d.%m.%Y')
        return HttpResponse(json.dumps(result), content_type="application/json")

save_dates_and_guests_ajax = SaveDatesAndGuestsAjaxView.as_view()


class SaveDateView(SaveDatesAndGuestsInSessionMixin, View):
    success_url = reverse_lazy('explore')
    form_class = DatesAndGuestsPostForm

    def post(self, request, *args, **kwargs):
        status, errors = self.save_dates_and_guests(request, set_anyway=True, prefix="index")
        if not status:
            for error in errors:
                messages.error(request, error)
        return HttpResponseRedirect(self.success_url)

save_dates_and_explore = SaveDateView.as_view()


class UploadFeaturedImageView(BusinessOwnerOnlyMixin, UploadImagesMixin, View):
    images_key = 'featured_image'

upload_featured_image = UploadFeaturedImageView.as_view()


class UploadGalleryImagesView(BusinessOwnerOnlyMixin, UploadImagesMixin, View):
    images_key = 'multiple_images'

upload_gallery_images = UploadGalleryImagesView.as_view()


class DeleteTempImageView(BusinessOwnerOnlyMixin, View):

    def post(self, request, *args, **kwargs):
        data = {}
        img_pk = request.POST.get('pk')
        try:
            img = TempFile.objects.get(pk=img_pk)
        except TempFile.DoesNotExist:
            pass
        else:
            img.delete()
        data['status'] = 'success'
        return JsonResponse(data)

delete_temp_image = DeleteTempImageView.as_view()
