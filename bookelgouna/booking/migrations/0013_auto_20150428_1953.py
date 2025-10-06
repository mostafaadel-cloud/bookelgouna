# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_auto_20150424_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='offline_booking_note',
            field=models.TextField(verbose_name='Note', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(related_name='orders', on_delete=django.db.models.deletion.SET_NULL, verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item_desc',
            field=models.TextField(verbose_name='Long Description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.IntegerField(default=1, verbose_name='Status', choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Rejected'), (4, 'No Show'), (5, 'Offline')]),
            preserve_default=True,
        ),
    ]
