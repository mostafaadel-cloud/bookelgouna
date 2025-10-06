# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0010_auto_20150512_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('for_long_term', models.BooleanField(default=False, verbose_name='For Long Term')),
                ('long_term_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('for_sale', models.BooleanField(default=False, verbose_name='For Sale')),
                ('sale_price', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('service', models.OneToOneField(related_name='options', verbose_name='Apartment', to='apartments.Apartment')),
            ],
            options={
                'verbose_name': 'Apartment Option',
                'verbose_name_plural': 'Apartment Options',
            },
            bases=(models.Model,),
        ),
    ]
