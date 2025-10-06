# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20150210_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessownerinfo',
            name='service_type',
            field=models.PositiveSmallIntegerField(verbose_name='Service Type', choices=[(0, 'Hotel'), (1, 'Apartment'), (2, 'TRANSPORT'), (3, 'Excursion'), (4, 'Sport'), (5, 'Other')]),
            preserve_default=True,
        ),
    ]
