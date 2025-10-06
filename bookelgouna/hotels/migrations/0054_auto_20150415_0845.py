# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0053_auto_20150415_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name=b'crop',
            field=image_cropping.fields.ImageRatioField('featured_image', '170x120', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop'),
            preserve_default=True,
        ),
    ]
