# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0019_hotel_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unapprovedhotel',
            options={'verbose_name': 'Hotel (unapproved)', 'verbose_name_plural': 'Hotels (unapproved)'},
        ),
        migrations.AlterModelOptions(
            name='unapprovedroom',
            options={'verbose_name': 'Room (unapproved)', 'verbose_name_plural': 'Rooms (unapproved)'},
        ),
    ]
