# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0018_auto_20150212_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Address', blank=True),
            preserve_default=True,
        ),
    ]
