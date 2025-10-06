# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import django.db.models.deletion
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'On moderation'), (1, 'Approved'), (2, 'Rejected'), (3, 'Updating')])),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Long Description')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Phone')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Rating', choices=[(0, 'One Star'), (1, 'Two Stars'), (2, 'Three Stars'), (3, 'Four Stars'), (4, 'Five Stars')])),
                ('duplicate', models.OneToOneField(related_name='origin', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hotels.Hotel', verbose_name='Duplicate')),
                ('owner', models.ForeignKey(related_name='services', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Hotel',
                'verbose_name_plural': 'Hotels',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                ('hotel', models.ForeignKey(related_name='images', verbose_name='Hotel', to='hotels.Hotel')),
            ],
            options={
                'verbose_name': 'Hotel Image',
                'verbose_name_plural': 'Hotel Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'On moderation'), (1, 'Approved'), (2, 'Rejected'), (3, 'Updating')])),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('area', models.FloatField(verbose_name='Area')),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image', blank=True)),
                ('duplicate', models.OneToOneField(related_name='origin', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='hotels.Room', verbose_name='Duplicate')),
                ('hotel', models.ForeignKey(verbose_name='Hotel', to='hotels.Hotel')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Room Type',
                'verbose_name_plural': 'Room Types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='hotels.RoomType'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UnapprovedHotel',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('hotels.hotel',),
        ),
    ]
