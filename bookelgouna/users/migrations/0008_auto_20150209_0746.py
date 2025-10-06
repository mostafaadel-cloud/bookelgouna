# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150209_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'avatar', '118x118', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping'),
            preserve_default=True,
        ),
    ]
