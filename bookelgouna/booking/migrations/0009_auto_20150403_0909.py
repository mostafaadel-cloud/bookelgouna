# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_auto_20150403_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item_desc',
            field=models.TextField(verbose_name='Item Description'),
            preserve_default=True,
        ),
    ]
