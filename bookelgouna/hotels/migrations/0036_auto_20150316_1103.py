# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0035_auto_20150316_0849'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MealPlanTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='hotels.MealPlan', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'hotels_mealplan_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoomPriceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('regular_price', models.FloatField(blank=True, null=True, verbose_name='Default price', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('pay_option', models.PositiveSmallIntegerField(default=1, verbose_name='Pay Option', choices=[(1, 'Free Cancellation'), (2, 'Non Refundable')])),
                ('item', models.ForeignKey(related_name='price_categories', verbose_name='Room', to='hotels.Room')),
                ('meal_plan', models.ForeignKey(verbose_name='Meal Plan', to='hotels.MealPlan')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoomPriceCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conditions', models.TextField(verbose_name='Conditions')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='hotels.RoomPriceCategory', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'hotels_roompricecategory_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='roompricecategorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='mealplantranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.RemoveField(
            model_name='roomprice',
            name='item',
        ),
        migrations.AddField(
            model_name='roomprice',
            name='price_category',
            field=models.ForeignKey(related_name='prices', verbose_name='Price Category', to='hotels.RoomPriceCategory', null=True),
            preserve_default=True,
        ),
    ]
