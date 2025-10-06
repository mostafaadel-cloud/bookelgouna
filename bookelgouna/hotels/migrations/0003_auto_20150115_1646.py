# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_auto_20150115_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='featured_image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Featured Image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotel',
            name='video_link',
            field=models.CharField(max_length=255, verbose_name='Video', blank=True),
            preserve_default=True,
        ),
    ]
