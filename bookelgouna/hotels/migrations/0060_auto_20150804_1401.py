# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators

MAX_ROOM_DESCRIPTION_LENGTH = 50


def shorten_price_category_name_field(apps, schema_editor):
    RoomPriceCategory = apps.get_model('hotels', 'RoomPriceCategory')
    for rpc in RoomPriceCategory.objects.all():
        for trans in rpc.translations.all():
            name = trans.name
            if len(name) > MAX_ROOM_DESCRIPTION_LENGTH:
                trans.name = name[:MAX_ROOM_DESCRIPTION_LENGTH]
                trans.save()


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0059_auto_20150804_1326'),
    ]

    operations = [
        migrations.RunPython(shorten_price_category_name_field, stub),
        migrations.AlterField(
            model_name='roompricecategorytranslation',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Category Name'),
            preserve_default=True,
        ),
        # verbose names changes
        migrations.AlterField(
            model_name='roomprice',
            name='price',
            field=models.FloatField(verbose_name='Price in USD', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roomtranslation',
            name='long_description',
            field=models.CharField(max_length=50, verbose_name='Room name'),
            preserve_default=True,
        ),
    ]
