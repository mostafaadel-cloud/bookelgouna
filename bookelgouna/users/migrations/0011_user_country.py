# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20150409_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=django_countries.fields.CountryField(default='EG', max_length=2, verbose_name=b'Country'),
            preserve_default=False,
        ),
    ]
