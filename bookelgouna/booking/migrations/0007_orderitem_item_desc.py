# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_orderitem_noshow_undo_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item_desc',
            field=models.TextField(verbose_name='Item Description', blank=True),
            preserve_default=True,
        ),
    ]
