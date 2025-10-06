# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20150320_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='noshow_undo_done',
            field=models.BooleanField(default=False, verbose_name='No show undo done once'),
            preserve_default=True,
        ),
    ]
