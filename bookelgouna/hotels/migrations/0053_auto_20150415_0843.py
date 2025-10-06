# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0052_auto_20150409_1235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='image',
            new_name='featured_image',
        ),
        migrations.RemoveField(
            model_name='room',
            name=b'cart_crop',
        ),
        migrations.AlterField(
            model_name='room',
            name=b'crop',
            field=image_cropping.fields.ImageRatioField('image', '170x120', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop'),
            preserve_default=True,
        ),
    ]
