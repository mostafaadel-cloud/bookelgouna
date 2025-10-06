# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_order_field(apps, schema_editor):
    Category = apps.get_model('blog', 'Category')
    order = 1
    for category in Category.objects.all():
        category.order = order
        category.save()
        order += 1


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20150416_0731'),
    ]

    operations = [
        migrations.RunPython(populate_order_field, stub),
    ]
