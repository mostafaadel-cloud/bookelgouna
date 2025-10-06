# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0010_room_number_of_beds'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(verbose_name='Price')),
                ('from_date', models.DateField(verbose_name='From Date')),
                ('to_date', models.DateField(verbose_name='To Date')),
                ('item', models.ForeignKey(related_name='prices', verbose_name='Room', to='hotels.Room')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
