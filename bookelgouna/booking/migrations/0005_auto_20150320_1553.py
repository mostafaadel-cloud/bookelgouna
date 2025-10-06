# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20150319_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantity'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.IntegerField(default=1, verbose_name='Status', choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Rejected'), (4, 'No Show')]),
            preserve_default=True,
        ),
    ]
