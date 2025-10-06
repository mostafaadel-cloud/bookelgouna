# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0048_hotelcomment_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name=b'cart_crop',
            field=image_cropping.fields.ImageRatioField('image', '170x120', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cart crop'),
            preserve_default=True,
        ),
    ]
