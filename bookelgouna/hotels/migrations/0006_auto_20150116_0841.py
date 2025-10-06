# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_auto_20150116_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='service',
            field=models.ForeignKey(related_name='items', verbose_name='Hotel', to='hotels.Hotel'),
            preserve_default=True,
        ),
    ]
