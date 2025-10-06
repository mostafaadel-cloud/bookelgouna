# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportitem',
            name=b'cart_crop',
            field=image_cropping.fields.ImageRatioField('featured_image', '170x120', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cart crop'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transportitem',
            name=b'crop',
            field=image_cropping.fields.ImageRatioField('featured_image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='transportreview',
            unique_together=set([('service', 'reviewer')]),
        ),
    ]
