# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0014_auto_20150210_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='long_description',
            field=models.TextField(default=b'Sample description', verbose_name='Long Description'),
            preserve_default=True,
        ),
    ]
