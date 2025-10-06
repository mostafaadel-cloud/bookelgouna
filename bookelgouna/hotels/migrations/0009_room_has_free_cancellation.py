# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_auto_20150116_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='has_free_cancellation',
            field=models.BooleanField(default=False, verbose_name='Has free cancellation'),
            preserve_default=True,
        ),
    ]
