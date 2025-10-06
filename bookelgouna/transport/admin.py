from django.core.urlresolvers import reverse
from hvad.admin import TranslatableAdmin
from hvad.forms import TranslatableModelForm
from image_cropping import ImageCroppingMixin

from django.contrib import admin

from common.admin import ApproveServiceAfterSaveMixin
from common.admin_utils import (ServiceTypeListFilter, PricesListFilter,
                                turn_off_review_mode, turn_on_review_mode, is_duplicate, view_on_site)

from .models import Transport, TransportImage, UnapprovedTransport, TransportReview, \
    ApprovedTransportComment, UnapprovedTransportComment, TransportItemImage, TransportItem, TransportItemDiscountPrice


class TransportImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class MyInlineModelAdmin(ImageCroppingMixin, admin.TabularInline):
    model = TransportImage


class TransportAdmin(ImageCroppingMixin, TranslatableAdmin):
    list_display = ('__unicode__', is_duplicate, 'slug', 'status', 'owner', 'review_mode',
                    'related_items', view_on_site)
    list_filter = ('status', ServiceTypeListFilter, PricesListFilter)
    inlines = [MyInlineModelAdmin]
    actions = [turn_on_review_mode, turn_off_review_mode]
    readonly_fields = ('status', is_duplicate, 'review_mode',)

    def __init__(self, *args, **kwargs):
        super(TransportAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ("title",)}

    def related_items(self, obj):
        obj = obj.origin if obj.is_duplicate() else obj
        if obj.items.exists():
            return '<a href="{}?service__id__exact={}"/>Show</a>'.format(
                reverse('admin:transport_transportitem_changelist'), obj.pk)
        else:
            return 'N/A'
    related_items.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('title', 'long_description')
            }),
            ('System Info', {
                'fields': ('slug', is_duplicate, 'review_mode', 'duplicate', 'status', 'owner', 'review_avg',
                           'review_num')
            }),
            ('General Info', {
                'fields': ('address',)
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
        return super(TransportAdmin, self).get_fieldsets(request, obj)


class UnapprovedTransportForm(TranslatableModelForm):
    def clean_owner(self):
        """
        prevent transport owner changing on moderation step
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.owner
        else:
            return self.cleaned_data['owner']

    class Meta:
        model = Transport


class UnapprovedTransportAdmin(ImageCroppingMixin, ApproveServiceAfterSaveMixin, TranslatableAdmin):
    list_display = ('__unicode__', 'slug', 'status', 'owner', view_on_site)
    inlines = [MyInlineModelAdmin]
    form = UnapprovedTransportForm

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
                'fields': ('address',)
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
        return super(UnapprovedTransportAdmin, self).get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('owner',)
        else:
            return ()

    def get_queryset(self, request):
        return super(UnapprovedTransportAdmin, self).get_queryset(request).filter(origin__isnull=False,
                                                                                  status=Transport.ON_MODERATION)


class TransportItemImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class TransportItemImageInline(ImageCroppingMixin, admin.TabularInline):
    model = TransportItemImage


class TransportItemDiscountAdminInline(admin.TabularInline):
    model = TransportItemDiscountPrice


class TransportItemAdmin(ImageCroppingMixin, TranslatableAdmin):
    inlines = [TransportItemImageInline, TransportItemDiscountAdminInline]
    list_display = ('__unicode__', 'type', 'slug', 'number', 'service', 'show_on_site')
    list_filter = ('service',)

    def __init__(self, *args, **kwargs):
        super(TransportItemAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ("type",)}

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Translatable', {
                'fields': ('title', 'long_description',)
            }),
            ('System Info', {
                'fields': ('slug', 'service', 'show_on_site')
            }),
            ('General Info', {
                'fields': ('type', 'number', 'price')
            }),
            ('Featured image', {
                'fields': ('featured_image',)
            })
        ]

        if obj is not None:
            del fieldsets[-1]
            fieldsets.append(
                ('Featured image and its cropping', {
                    'fields': (('featured_image', 'crop', 'cart_crop'),)
                })
            )
        self.fieldsets = fieldsets
        return super(TransportItemAdmin, self).get_fieldsets(request, obj)


class ApprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class UnapprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class TransportReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transport, TransportAdmin)
admin.site.register(UnapprovedTransport, UnapprovedTransportAdmin)
admin.site.register(TransportImage, TransportImageAdmin)
admin.site.register(TransportReview, TransportReviewAdmin)
admin.site.register(TransportItem, TransportItemAdmin)
admin.site.register(TransportItemImage, TransportItemImageAdmin)
admin.site.register(ApprovedTransportComment, ApprovedCommentAdmin)
admin.site.register(UnapprovedTransportComment, UnapprovedCommentAdmin)
