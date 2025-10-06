# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib import messages


class PricesListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'item prices'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'has_prices'

    YES = 'yes'
    NO = 'no'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (self.YES, 'has prices'),
            (self.NO, 'has no prices'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value() == self.YES:
            return queryset.has_prices()
        if self.value() == self.NO:
            return queryset.has_no_prices()


class ServiceTypeListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'type'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'type'

    ORIGINAL = '1'
    DUPLICATE = '2'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (self.ORIGINAL, 'origin'),
            (self.DUPLICATE, 'duplicate'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value() == self.ORIGINAL:
            return queryset.originals()
        if self.value() == self.DUPLICATE:
            return queryset.duplicates()


def turn_on_review_mode(modeladmin, request, queryset):
    originals = queryset.originals().filter(review_mode=False)
    if not queryset.originals().exists():
        modeladmin.message_user(request, 'Use this action on originals only.', messages.WARNING)
    queryset.model.objects.filter(origin__in=originals).update(review_mode=True)
    number = originals.update(review_mode=True)
    modeladmin.message_user(request, 'Review mode was turned ON for {} service(s).'.format(number),
                            messages.INFO if number > 0 else messages.WARNING)
turn_on_review_mode.short_description = 'Turn on review mode for selected original services'


def turn_off_review_mode(modeladmin, request, queryset):
    originals = queryset.originals().filter(review_mode=True)
    if not queryset.originals().exists():
        modeladmin.message_user(request, 'Use this action on originals only.', messages.WARNING)
    queryset.model.objects.filter(origin__in=originals).update(review_mode=False)
    number = originals.update(review_mode=False)
    modeladmin.message_user(request, 'Review mode was turned OFF for {} service(s).'.format(number),
                            messages.INFO if number > 0 else messages.WARNING)
turn_off_review_mode.short_description = 'Turn off review mode for selected original services'


def is_duplicate(obj):
    return obj.is_duplicate()
is_duplicate.boolean = True


def view_on_site(obj):
    return '<a href="%s">view on site</a>' % obj.get_absolute_url()
view_on_site.allow_tags = True
view_on_site.short_description = 'View on site'
