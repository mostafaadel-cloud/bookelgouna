# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0012_auto_20150527_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='review_mode',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmentpricecategory',
            name='pay_option',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Pay Options', choices=[(1, 'Free Cancellation'), (2, 'Non Refundable')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmentpricecategory',
            name='regular_price',
            field=models.FloatField(verbose_name='Regular price', validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmentpricecategorytranslation',
            name='conditions',
            field=models.TextField(verbose_name='Terms & Conditions'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmentpricecategorytranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmenttranslation',
            name='long_description',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmenttranslation',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Short Description'),
            preserve_default=True,
        ),
    ]
