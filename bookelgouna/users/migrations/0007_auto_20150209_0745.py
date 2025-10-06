# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150118_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=image_cropping.fields.ImageCropField(upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'image', '118x118', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping'),
            preserve_default=True,
        ),
    ]
