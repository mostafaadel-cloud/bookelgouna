# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0043_auto_20150319_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name=b'big_crop',
            field=image_cropping.fields.ImageRatioField('featured_image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='big crop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotel',
            name=b'small_crop',
            field=image_cropping.fields.ImageRatioField('featured_image', '138x135', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='small crop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotelimage',
            name=b'big_crop',
            field=image_cropping.fields.ImageRatioField('image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='big crop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotelimage',
            name=b'small_crop',
            field=image_cropping.fields.ImageRatioField('image', '138x135', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='small crop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name=b'crop',
            field=image_cropping.fields.ImageRatioField('image', '147x130', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop'),
            preserve_default=True,
        ),
    ]
