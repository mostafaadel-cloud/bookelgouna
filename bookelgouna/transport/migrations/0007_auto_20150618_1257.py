# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0006_auto_20150528_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='review_mode',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transportitem',
            name='number',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Item Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transportitemtranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transportitemtranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transporttranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transporttranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
    ]
