# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0004_transportitemtranslation_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportitem',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Type', choices=[(1, 'One Ride'), (2, 'Rent')]),
            preserve_default=True,
        ),
    ]
