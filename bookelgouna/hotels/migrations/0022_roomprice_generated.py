# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0021_auto_20150213_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomprice',
            name='generated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
