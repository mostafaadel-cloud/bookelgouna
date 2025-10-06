# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from adminsortable.admin import SortableAdminMixin
from hvad.admin import TranslatableAdmin, TranslatableTabularInline
from hvad.forms import TranslatableModelForm
from image_cropping import ImageCroppingMixin

from django import forms
from django.core.urlresolvers import reverse
from django.contrib import admin

from common.admin import ApproveServiceAfterSaveMixin
from common.admin_utils import ServiceTypeListFilter, PricesListFilter, turn_on_review_mode, \
    turn_off_review_mode, is_duplicate, view_on_site

from .models import Hotel, HotelImage, UnapprovedHotel, RoomType, Room, RoomPrice, HotelReview, \
    ApprovedHotelComment, UnapprovedHotelComment, RoomPriceCategory, MealPlan, HotelAmenityCategory, \
    HotelAmenity, RoomAmenity


class HotelImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class MyInlineModelAdmin(ImageCroppingMixin, admin.TabularInline):
    model = HotelImage


class HotelAmenityModelAdminInline(admin.TabularInline):
    model = Hotel.amenities.through


class HotelAdmin(ImageCroppingMixin, TranslatableAdmin):
    list_display = ('__unicode__', is_duplicate, 'slug', 'status', 'owner', 'review_mode',
                    'related_items', view_on_site)
    list_filter = ('status', ServiceTypeListFilter, PricesListFilter)
    inlines = [MyInlineModelAdmin, HotelAmenityModelAdminInline]
    actions = [turn_on_review_mode, turn_off_review_mode]
    readonly_fields = ('status', is_duplicate, 'review_mode',)

    def __init__(self, *args, **kwargs):
        super(HotelAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ("title",)}

    def related_items(self, obj):
        obj = obj.origin if obj.is_duplicate() else obj
        if obj.items.exists():
            return '<a href="{}?service__id__exact={}"/>Show</a>'.format(
                reverse('admin:hotels_room_changelist'), obj.pk)
        else:
            return 'N/A'
    related_items.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('title', 'long_description')
            }),
            ('System Info', {
                'fields': ('slug', is_duplicate, 'review_mode', 'duplicate', 'status', 'owner',
                           'review_avg', 'review_num')
            }),
            ('General Info', {
                'fields': ('address', 'rating')
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
        return super(HotelAdmin, self).get_fieldsets(request, obj)


class UnapprovedHotelForm(TranslatableModelForm):
    def clean_owner(self):
        """
        prevent hotel owner changing on moderation step
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.owner
        else:
            return self.cleaned_data['owner']

    class Meta:
        model = UnapprovedHotel


class UnapprovedHotelAdmin(ImageCroppingMixin, ApproveServiceAfterSaveMixin, TranslatableAdmin):
    list_display = ('__unicode__', 'slug', 'status', 'owner', view_on_site)
    inlines = [MyInlineModelAdmin, HotelAmenityModelAdminInline]
    form = UnapprovedHotelForm

    def has_add_permission(self, request):
        return False

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('title', 'long_description')
            }),
            ('System Info', {
                'fields': ('status', 'slug')
            }),
            ('General Info', {
                'fields': ('address', 'rating')
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
        return super(UnapprovedHotelAdmin, self).get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('owner',)
        else:
            return ()

    def get_queryset(self, request):
        return super(UnapprovedHotelAdmin, self).get_queryset(request).filter(origin__isnull=False,
                                                                              status=Hotel.ON_MODERATION)


class MealPlanForm(TranslatableModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        q = MealPlan.objects.language('all').filter(name=name)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The meal plan with this Name already exists.")
        return name


class MealPlanAdmin(TranslatableAdmin):
    list_display = ('__unicode__',)
    form = MealPlanForm


class RoomPriceAdminInline(admin.TabularInline):
    model = RoomPrice
    extra = 1


class RoomPriceCategoryAdmin(TranslatableAdmin):
    inlines = [RoomPriceAdminInline]

    def __init__(self, *args, **kwargs):
        super(RoomPriceCategoryAdmin, self).__init__(*args, **kwargs)
        self.fieldsets = (
            ('Translatable', {
                'fields': ('name', 'conditions',)
            }),
            ('General Info', {
                'fields': ('item', 'type', 'regular_price', 'pay_option', 'meal_plan')
            })
        )


class RoomPriceCategoryInline(TranslatableTabularInline):
    model = RoomPriceCategory
    readonly_fields = ('changeform_link',)

    def __init__(self, *args, **kwargs):
        super(RoomPriceCategoryInline, self).__init__(*args, **kwargs)
        self.fields = ('regular_price', 'pay_option', 'meal_plan', 'conditions', 'changeform_link')

    def changeform_link(self, obj):
        if obj.id:
            changeform_url = reverse(
                'admin:hotels_roompricecategory_change', args=(obj.id,)
            )
            return u'<a href="%s" target="_blank">Details</a>' % changeform_url
        return u''
    changeform_link.allow_tags = True
    changeform_link.short_description = ''   # omit column header


class RoomAmenityModelAdminInline(admin.TabularInline):
    model = Room.amenities.through


class RoomAdmin(ImageCroppingMixin, TranslatableAdmin):
    inlines = [RoomPriceCategoryInline, RoomAmenityModelAdminInline]
    list_display = ('__unicode__', 'slug', 'allotment', 'service', 'show_on_site')
    list_filter = ('service',)

    def __init__(self, *args, **kwargs):
        super(RoomAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ('long_description',)}

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('long_description',)
            }),
            ('System Info', {
                'fields': ('slug', 'service', 'show_on_site')
            }),
            ('General Info', {
                'fields': ('allotment', 'area', 'adults', 'children', 'has_sea_views',
                           'has_air_conditioning')
            }),
            ('Featured image', {
                'fields': ('featured_image',)
            })
        ]

        if obj is not None:
            del fieldsets[-1]
            fieldsets.append(
                ('Featured image and its cropping', {
                    'fields': (('featured_image', 'crop'),)
                })
            )
        self.fieldsets = fieldsets
        return super(RoomAdmin, self).get_fieldsets(request, obj)


class RoomTypeForm(TranslatableModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        q = RoomType.objects.language('all').filter(name=name)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The room type with this Name already exists.")
        return name


class RoomTypeAdmin(TranslatableAdmin):
    form = RoomTypeForm


class RoomPriceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'price_category', 'price', 'from_date', 'to_date')


class HotelAmenityCategoryForm(TranslatableModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        q = HotelAmenityCategory.objects.language('all').filter(name=name)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The amenity category with this Name already exists.")
        return name


class HotelAmenityCategoryAdmin(SortableAdminMixin, TranslatableAdmin):
    # list_display = ('__unicode__',)
    form = HotelAmenityCategoryForm


class HotelAmenityForm(TranslatableModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        q = HotelAmenity.objects.language('all').filter(name=name)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The hotel amenity with this Name already exists.")
        return name


class HotelAmenityAdmin(TranslatableAdmin):
    list_display = ('__unicode__', 'category')
    ordering = ('category__order',)
    form = HotelAmenityForm


# class RoomAmenityCategoryForm(TranslatableModelForm):
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         q = RoomAmenityCategory.objects.language('all').filter(name=name)
#         if self.instance.pk:
#             q = q.exclude(pk=self.instance.pk)
#         if q.exists():
#             raise forms.ValidationError("The amenity category with this Name already exists.")
#         return name
#
#
# class RoomAmenityCategoryAdmin(TranslatableAdmin):
#     list_display = ('__unicode__',)
#     form = RoomAmenityCategoryForm


class RoomAmenityForm(TranslatableModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        q = RoomAmenity.objects.language('all').filter(name=name)
        if self.instance.pk:
            q = q.exclude(pk=self.instance.pk)
        if q.exists():
            raise forms.ValidationError("The room amenity with this Name already exists.")
        return name


class RoomAmenityAdmin(TranslatableAdmin):
    list_display = ('__unicode__',)
    form = RoomAmenityForm


class ApprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class UnapprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class HotelReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hotel, HotelAdmin)
admin.site.register(UnapprovedHotel, UnapprovedHotelAdmin)
admin.site.register(HotelImage, HotelImageAdmin)
admin.site.register(HotelReview, HotelReviewAdmin)
admin.site.register(MealPlan, MealPlanAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(RoomPriceCategory, RoomPriceCategoryAdmin)
admin.site.register(RoomPrice, RoomPriceAdmin)
admin.site.register(HotelAmenityCategory, HotelAmenityCategoryAdmin)
admin.site.register(HotelAmenity, HotelAmenityAdmin)
admin.site.register(RoomAmenity, RoomAmenityAdmin)
# admin.site.register(RoomAmenityCategory, RoomAmenityCategoryAdmin)
admin.site.register(ApprovedHotelComment, ApprovedCommentAdmin)
admin.site.register(UnapprovedHotelComment, UnapprovedCommentAdmin)
