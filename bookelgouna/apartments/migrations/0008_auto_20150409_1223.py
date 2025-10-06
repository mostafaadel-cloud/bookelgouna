# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0007_auto_20150403_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'verbose_name': 'Apartment', 'verbose_name_plural': 'APARTMENTS'},
        ),
        migrations.AlterField(
            model_name='apartmentcomment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='is approved'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmentpricecategorytranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category Name:'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='apartmentreview',
            unique_together=set([('service', 'reviewer')]),
        ),
    ]
