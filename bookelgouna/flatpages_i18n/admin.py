from adminsortable.admin import SortableAdminMixin
from hvad.admin import TranslatableAdmin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import FlatpageForm
from .models import FlatPage


class FlatPageAdmin(SortableAdminMixin, TranslatableAdmin):
    form = FlatpageForm
    list_display = ('__unicode__', 'created', 'modified', 'is_published')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url',)

    def __init__(self, *args, **kwargs):
        super(FlatPageAdmin, self).__init__(*args, **kwargs)
        self.fieldsets = (
            (_('Translatable'), {'fields': ('title', 'desc_metatag', 'content')}),
            (_('Other Info'), {'fields': ('url', 'is_published', 'sites')}),
            (_('Advanced options'), {'classes': ('collapse',), 'fields': ('registration_required', 'template_name')}),
        )


admin.site.register(FlatPage, FlatPageAdmin)
