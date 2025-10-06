# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0007_auto_20150618_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransportItemDiscountPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_days', models.SmallIntegerField(verbose_name='Number of days', validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(30)])),
                ('discount_price', models.FloatField(verbose_name='Discount price', validators=[django.core.validators.MinValueValidator(0.01)])),
                ('item', models.ForeignKey(related_name='discount_prices', verbose_name='Transport Item', to='transport.TransportItem')),
            ],
            options={
                'ordering': ('number_of_days',),
                'verbose_name': 'Transport Item Discount Price',
                'verbose_name_plural': 'Transport Item Discount Prices',
            },
            bases=(models.Model,),
        ),
    ]
