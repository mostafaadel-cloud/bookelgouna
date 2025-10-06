# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hvad.admin import TranslatableAdmin, TranslatableTabularInline
from hvad.forms import TranslatableModelForm
from image_cropping import ImageCroppingMixin

from django import forms
from django.core.urlresolvers import reverse
from django.contrib import admin

from common.admin import ApproveServiceAfterSaveMixin
from common.admin_utils import (ServiceTypeListFilter, PricesListFilter, turn_off_review_mode, turn_on_review_mode,
                                is_duplicate, view_on_site)

from .models import Apartment, ApartmentImage, UnapprovedApartment, \
    ApartmentReview, ApprovedApartmentComment, UnapprovedApartmentComment, \
    ApartmentAmenity, ApartmentPrice, ApartmentPriceCategory, ApartmentOptions


class ApartmentImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class MyInlineModelAdmin(ImageCroppingMixin, admin.TabularInline):
    model = ApartmentImage


class ApartmentAmenityModelAdminInline(admin.TabularInline):
    model = Apartment.amenities.through


class ApartmentAdmin(ImageCroppingMixin, TranslatableAdmin):
    list_display = ('__unicode__', is_duplicate, 'slug', 'status', 'owner', 'review_mode', view_on_site)
    list_filter = ('status', ServiceTypeListFilter, PricesListFilter)
    inlines = [MyInlineModelAdmin, ApartmentAmenityModelAdminInline]
    actions = [turn_on_review_mode, turn_off_review_mode]
    readonly_fields = ('status', is_duplicate, 'review_mode',)

    def __init__(self, *args, **kwargs):
        super(ApartmentAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ("title",)}

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('title', 'long_description')
            }),
            ('System Info', {
                'fields': ('slug', is_duplicate, 'review_mode', 'duplicate', 'show_on_site', 'status', 'owner',
                           'review_avg', 'review_num')
            }),
            ('General Info', {
                'fields': ('address', 'type', 'number_of_rooms', 'adults', 'children', 'min_nights_to_book')
            }),
            ('Featured image', {
                'fields': ('featured_image',)
            })
        ]

        if obj is not None:
            del fieldsets[-1]
            fieldsets.append(
                ('Featured image and its cropping', {
                    'fields': (('featured_image', 'big_crop', 'small_crop'),)
                })
            )
        self.fieldsets = fieldsets
        return super(ApartmentAdmin, self).get_fieldsets(request, obj)


class UnapprovedApartmentForm(TranslatableModelForm):
    def clean_owner(self):
        """
        prevent Apartment owner changing on moderation step
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.owner
        else:
            return self.cleaned_data['owner']

    class Meta:
        model = Apartment


class UnapprovedApartmentAdmin(ImageCroppingMixin, ApproveServiceAfterSaveMixin, TranslatableAdmin):
    list_display = ('__unicode__', 'slug', 'status', 'owner', view_on_site)
    inlines = [MyInlineModelAdmin, ApartmentAmenityModelAdminInline]
    form = UnapprovedApartmentForm

    def has_add_permission(self, request):
        return False

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('title', 'long_description')
            }),
            ('System Info', {
                'fields': ('status', 'show_on_site', 'slug')
            }),
            ('General Info', {
                'fields': ('address', 'type', 'number_of_rooms', 'adults', 'children', 'min_nights_to_book')
            }),
            ('Featured image', {
                'fields': ('featured_image',)
            })
        ]

        if obj is not None:
            del fieldsets[-1]
            fieldsets.append(
                ('Featured image and its cropping', {
                    'fields': (('featured_image', 'big_crop', 'small_crop'),)
                })
            )
        self.fieldsets = fieldsets
        return super(UnapprovedApartmentAdmin, self).get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('owner',)
        else:
            return ()

    def get_queryset(self, request):
        return super(UnapprovedApartmentAdmin, self).get_queryset(request).filter(origin__isnull=False,
                                                                                  status=Apartment.ON_MODERATION)


class ApartmentPriceAdminInline(admin.TabularInline):
    model = ApartmentPrice
    extra = 1


class ApartmentPriceCategoryAdmin(TranslatableAdmin):
    inlines = [ApartmentPriceAdminInline]

    def __init__(self, *args, **kwargs):
        super(ApartmentPriceCategoryAdmin, self).__init__(*args, **kwargs)
        self.fieldsets = (
            ('Translatable', {
                'fields': ('name', 'conditions',)
            }),
            ('General Info', {
                'fields': ('item', 'regular_price', 'pay_option')
            })
        )


class ApartmentPriceCategoryInline(TranslatableTabularInline):
    model = ApartmentPriceCategory
    readonly_fields = ('changeform_link',)

    def __init__(self, *args, **kwargs):
        super(ApartmentPriceCategoryInline, self).__init__(*args, **kwargs)
        self.fields = ('regular_price', 'pay_option', 'meal_plan', 'conditions', 'changeform_link')

    def changeform_link(self, obj):
        if obj.id:
            changeform_url = reverse(
                'admin:apartments_apartmentpricecategory_change', args=(obj.id,)
            )
            return u'<a href="%s" target="_blank">Details</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header

class ApartmentPriceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'price_category', 'price', 'from_date', 'to_date')


class ApartmentOptionsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'for_long_term', 'long_term_price', 'for_sale', 'sale_price')

class ApartmentAmenityForm(TranslatableModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        q = ApartmentAmenity.objects.language('all').filter(name=name)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The Apartment amenity with this Name already exists.")
        return name


class ApartmentAmenityAdmin(TranslatableAdmin):
    list_display = ('__unicode__',)
    form = ApartmentAmenityForm


class ApprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class UnapprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class ApartmentReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(UnapprovedApartment, UnapprovedApartmentAdmin)
admin.site.register(ApartmentImage, ApartmentImageAdmin)
admin.site.register(ApartmentReview, ApartmentReviewAdmin)
admin.site.register(ApartmentPriceCategory, ApartmentPriceCategoryAdmin)
admin.site.register(ApartmentPrice, ApartmentPriceAdmin)
admin.site.register(ApartmentOptions, ApartmentOptionsAdmin)
admin.site.register(ApartmentAmenity, ApartmentAmenityAdmin)
admin.site.register(ApprovedApartmentComment, ApprovedCommentAdmin)
admin.site.register(UnapprovedApartmentComment, UnapprovedCommentAdmin)
