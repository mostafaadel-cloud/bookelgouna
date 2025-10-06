# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessownerinfo',
            name='allowed_types',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=11, null=True, choices=[(0, 'Hotel'), (1, 'Apartment'), (2, 'Transport'), (3, 'Excursion'), (4, 'Sport'), (5, 'Entertainment')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='base_account',
            field=models.ForeignKey(related_name='subaccounts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.PositiveIntegerField(default=1, null=True, verbose_name='Type', blank=True, choices=[(1, 'End User'), (2, 'Business Owner'), (3, 'Travel Agency')]),
            preserve_default=True,
        ),
    ]
