# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0056_auto_20150527_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='review_mode',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hoteltranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hoteltranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='has_sea_views',
            field=models.BooleanField(default=False, verbose_name='Sea view'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roompricecategory',
            name='pay_option',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Pay Options', choices=[(1, 'Free Cancellation'), (2, 'Non Refundable')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roompricecategory',
            name='regular_price',
            field=models.FloatField(verbose_name='Regular price', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roompricecategorytranslation',
            name='conditions',
            field=models.TextField(verbose_name='Terms & Conditions'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roompricecategorytranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roomtranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
    ]
