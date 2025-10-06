# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hvad.admin import TranslatableAdmin

from django.contrib import admin

from .models import BookingEmailTemplate


class BookingEmailTemplateAdmin(TranslatableAdmin):
    list_display = ('__unicode__', 'trans')

    def trans(self, obj):
        return ', '.join(obj.translations.order_by('language_code').values_list('language_code', flat=True))
    trans.short_description = 'Translated into'


admin.site.register(BookingEmailTemplate, BookingEmailTemplateAdmin)
