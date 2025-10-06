# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0033_auto_20150313_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomtranslation',
            name='title',
        ),
        migrations.AlterField(
            model_name='hoteltranslation',
            name='long_description',
            field=models.TextField(verbose_name='Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roomtranslation',
            name='long_description',
            field=models.TextField(verbose_name='Description'),
            preserve_default=True,
        ),
    ]
