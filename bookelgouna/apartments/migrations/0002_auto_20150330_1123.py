# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(verbose_name='Price', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('from_date', models.DateField(verbose_name='From Date')),
                ('to_date', models.DateField(verbose_name='To Date')),
                ('generated', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Apartment Price',
                'verbose_name_plural': 'Apartment Prices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentPriceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('regular_price', models.FloatField(blank=True, null=True, verbose_name='Regular Price', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('pay_option', models.PositiveSmallIntegerField(default=1, verbose_name='Pay Option', choices=[(1, 'Free Cancellation'), (2, 'Non Refundable')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('apartment', models.OneToOneField(related_name='price_category', verbose_name='Apartment', to='apartments.Apartment')),
            ],
            options={
                'verbose_name': 'Room Price Category',
                'verbose_name_plural': 'Room Price Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentPriceCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Category Name')),
                ('conditions', models.TextField(verbose_name='Conditions')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='apartments.ApartmentPriceCategory', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'apartments_apartmentpricecategory_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='apartmentpricecategorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='apartmentprice',
            name='price_category',
            field=models.ForeignKey(related_name='prices', verbose_name='Price Category', to='apartments.ApartmentPriceCategory', null=True),
            preserve_default=True,
        ),
    ]
