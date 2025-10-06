# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150109_1103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessownerinfo',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default="+380671111111", max_length=128, verbose_name='Phone'),
            preserve_default=False,
        ),
    ]
