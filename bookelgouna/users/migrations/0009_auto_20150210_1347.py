# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150209_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=image_cropping.fields.ImageCropField(upload_to=b'', verbose_name='Avatar', blank=True),
            preserve_default=True,
        ),
    ]
