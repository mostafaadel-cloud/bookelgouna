# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessownerinfo',
            name='service_type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Service Type', choices=[(1, 'Hotel'), (2, 'Apartment'), (3, 'Transport'), (4, 'Excursion'), (5, 'Sport'), (6, 'Other')]),
            preserve_default=False,
        ),
    ]
