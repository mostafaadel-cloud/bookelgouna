# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from hvad.manager import TranslationQueryset, FallbackQueryset

from django.db.models import Q, QuerySet


class SimplePricesMixin(object):
    """
    transports, sports, excursions, entertainment items has simple prices and the same structure
    """
    def originals(self):
        return self.filter(origin__isnull=True)

    def duplicates(self):
        return self.filter(origin__isnull=False)

    def has_prices(self):
        return self.filter(Q(items__isnull=False) | Q(origin__items__isnull=False)).distinct()

    def has_no_prices(self):
        return self.exclude(items__isnull=False).exclude(origin__items__isnull=False)


class SimplePricesTranslationQueryset(SimplePricesMixin, TranslationQueryset):
    pass


class SimplePricesFallbackQueryset(SimplePricesMixin, FallbackQueryset):
    pass


class SimplePricesQueryset(SimplePricesMixin, QuerySet):
    pass
