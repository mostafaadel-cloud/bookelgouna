# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0024_auto_20150311_0748'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='Slug', blank=True),
            preserve_default=True,
        ),
    ]
