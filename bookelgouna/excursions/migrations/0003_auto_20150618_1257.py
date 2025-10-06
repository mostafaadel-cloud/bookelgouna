# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0002_auto_20150528_1004'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excursion',
            options={'verbose_name': 'Excursion', 'verbose_name_plural': 'EXCURSIONS'},
        ),
        migrations.AddField(
            model_name='excursion',
            name='review_mode',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursioncomment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='is approved'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursionitem',
            name='number',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Item Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursionitemtranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursionitemtranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursiontranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursiontranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
    ]
