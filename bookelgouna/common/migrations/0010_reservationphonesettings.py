# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_auto_20150528_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationPhoneSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=50)),
                ('enabled_for_services', multiselectfield.db.fields.MultiSelectField(default=[0, 1, 2, 3, 4, 5], max_length=11, choices=[(0, 'Hotel'), (1, 'Apartment'), (2, 'Transport'), (3, 'Excursion'), (4, 'Sport'), (5, 'Entertainment')])),
                ('is_enabled', models.BooleanField(default=True, help_text='Has the most priority. If set to False then phone is not displayed at all regardless of "enabled_for_services" field value')),
            ],
            options={
                'verbose_name': 'Reservation phone settings',
                'verbose_name_plural': 'Reservation phone settings',
            },
            bases=(models.Model,),
        ),
    ]
