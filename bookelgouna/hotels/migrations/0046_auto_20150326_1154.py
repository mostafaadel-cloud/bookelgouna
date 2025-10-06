# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0045_auto_20150325_0641'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelAmenity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Hotel Amenity',
                'verbose_name_plural': 'Hotel Amenities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HotelAmenityCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Hotel Amenity Category',
                'verbose_name_plural': 'Hotel Amenity Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HotelAmenityCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='hotels.HotelAmenityCategory', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'hotels_hotelamenitycategory_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HotelAmenityTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='hotels.HotelAmenity', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'hotels_hotelamenity_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoomAmenity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Room Amenity',
                'verbose_name_plural': 'Room Amenities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoomAmenityTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='hotels.RoomAmenity', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'hotels_roomamenity_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='roomamenitytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='hotelamenitytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='hotelamenitycategorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='hotelamenity',
            name='category',
            field=models.ForeignKey(related_name='amenities', verbose_name='Category', to='hotels.HotelAmenityCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotel',
            name='amenities',
            field=models.ManyToManyField(related_name='services', verbose_name='Amenities', to='hotels.HotelAmenity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='amenities',
            field=models.ManyToManyField(related_name='items', verbose_name='Amenities', to='hotels.RoomAmenity'),
            preserve_default=True,
        ),
    ]
