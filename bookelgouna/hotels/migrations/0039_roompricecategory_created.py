# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0038_auto_20150316_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='roompricecategory',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 17, 13, 23, 27, 815578, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
