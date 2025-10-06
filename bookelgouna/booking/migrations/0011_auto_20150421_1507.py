# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_auto_20150409_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='from_date',
            field=models.DateTimeField(verbose_name='From Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='to_date',
            field=models.DateTimeField(verbose_name='To Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='from_date',
            field=models.DateTimeField(verbose_name='From Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='to_date',
            field=models.DateTimeField(verbose_name='To Date'),
            preserve_default=True,
        ),
    ]
