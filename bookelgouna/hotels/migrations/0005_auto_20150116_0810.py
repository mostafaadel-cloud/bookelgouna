# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0004_auto_20150116_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnapprovedRoom',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('hotels.room',),
        ),
        migrations.RenameField(
            model_name='hotelimage',
            old_name='hotel',
            new_name='service',
        ),
    ]
