# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_businessownerinfo_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessownerinfo',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Phone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='businessownerinfo',
            name='service_type',
            field=models.PositiveSmallIntegerField(verbose_name='Service Type', choices=[(0, 'Hotel'), (1, 'Apartment'), (2, 'Transport'), (3, 'Excursion'), (4, 'Sport'), (5, 'Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='businessownerinfo',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=True,
        ),
    ]
