# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_price_category_names(apps, schema_editor):
    Room = apps.get_model('hotels', 'Room')
    s = "%s price category %d"
    for room in Room.objects.prefetch_related('price_categories', 'price_categories__translations'):
        counter = 1
        for price_category in room.price_categories.all():
            for trans in price_category.translations.all():
                language_code = trans.language_code
                if trans.name == u'':
                    trans.name = s % (language_code, counter)
                    trans.save()
            counter += 1


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0041_auto_20150319_1630'),
    ]

    operations = [
        migrations.RunPython(add_price_category_names, stub),
    ]
