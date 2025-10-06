# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20150305_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='is_enabled',
            field=models.BooleanField(default=False, verbose_name='is enabled'),
            preserve_default=True,
        ),
    ]
