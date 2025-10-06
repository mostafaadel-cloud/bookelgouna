# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entertainment', '0002_auto_20150528_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='entertainment',
            name='review_mode',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entertainmentitem',
            name='number',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Item Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entertainmentitem',
            name='type',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Type', choices=[(1, 'One Time'), (2, 'Price Per Day')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entertainmentitemtranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entertainmentitemtranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entertainmenttranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entertainmenttranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
    ]
