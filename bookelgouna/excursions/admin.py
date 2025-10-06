from hvad.admin import TranslatableAdmin
from hvad.forms import TranslatableModelForm
from image_cropping import ImageCroppingMixin

from django.contrib import admin
from django.core.urlresolvers import reverse

from common.admin import ApproveServiceAfterSaveMixin
from common.admin_utils import PricesListFilter, ServiceTypeListFilter, turn_on_review_mode, \
    turn_off_review_mode, is_duplicate, view_on_site

from .models import Excursion, ExcursionImage, UnapprovedExcursion, ExcursionReview, \
    ApprovedExcursionComment, UnapprovedExcursionComment, ExcursionItemImage, ExcursionItem, ExcursionItemDiscountPrice


class ExcursionImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class MyInlineModelAdmin(ImageCroppingMixin, admin.TabularInline):
    model = ExcursionImage


class ExcursionAdmin(ImageCroppingMixin, TranslatableAdmin):
    list_display = ('__unicode__', is_duplicate, 'slug', 'status', 'owner', 'review_mode',
                    'related_items', view_on_site)
    list_filter = ('status', ServiceTypeListFilter, PricesListFilter)
    inlines = [MyInlineModelAdmin]
    actions = [turn_on_review_mode, turn_off_review_mode]
    readonly_fields = ('status', is_duplicate, 'review_mode',)

    def __init__(self, *args, **kwargs):
        super(ExcursionAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields = {'slug': ("title",)}

    def related_items(self, obj):
        obj = obj.origin if obj.is_duplicate() else obj
        if obj.items.exists():
            return '<a href="{}?service__id__exact={}"/>Show</a>'.format(
                reverse('admin:excursions_excursionitem_changelist'), obj.pk)
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
        return super(ExcursionAdmin, self).get_fieldsets(request, obj)


class UnapprovedExcursionForm(TranslatableModelForm):
    def clean_owner(self):
        """
        prevent excursion owner changing on moderation step
        """
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.owner
        else:
            return self.cleaned_data['owner']

    class Meta:
        model = Excursion


class UnapprovedExcursionAdmin(ImageCroppingMixin, ApproveServiceAfterSaveMixin, TranslatableAdmin):
    list_display = ('__unicode__', 'slug', 'status', 'owner', view_on_site)
    inlines = [MyInlineModelAdmin]
    form = UnapprovedExcursionForm

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
        return super(UnapprovedExcursionAdmin, self).get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('owner',)
        else:
            return ()

    def get_queryset(self, request):
        return super(UnapprovedExcursionAdmin, self).get_queryset(request).filter(origin__isnull=False,
                                                                                  status=Excursion.ON_MODERATION)


class ExcursionItemImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class ExcursionItemImageInline(ImageCroppingMixin, admin.TabularInline):
    model = ExcursionItemImage


class ExcursionItemDiscountAdminInline(admin.TabularInline):
    model = ExcursionItemDiscountPrice


class ExcursionItemAdmin(ImageCroppingMixin, TranslatableAdmin):
    inlines = [ExcursionItemImageInline, ExcursionItemDiscountAdminInline]
    list_display = ('__unicode__', 'type', 'slug', 'number', 'service', 'show_on_site')
    list_filter = ('service',)

    def __init__(self, *args, **kwargs):
        super(ExcursionItemAdmin, self).__init__(*args, **kwargs)
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
        return super(ExcursionItemAdmin, self).get_fieldsets(request, obj)


class ApprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class UnapprovedCommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'creator', 'entity', 'created', 'is_approved')


class ExcursionReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Excursion, ExcursionAdmin)
admin.site.register(UnapprovedExcursion, UnapprovedExcursionAdmin)
admin.site.register(ExcursionImage, ExcursionImageAdmin)
admin.site.register(ExcursionReview, ExcursionReviewAdmin)
admin.site.register(ExcursionItem, ExcursionItemAdmin)
admin.site.register(ExcursionItemImage, ExcursionItemImageAdmin)
admin.site.register(ApprovedExcursionComment, ApprovedCommentAdmin)
admin.site.register(UnapprovedExcursionComment, UnapprovedCommentAdmin)
