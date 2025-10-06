# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0042_auto_20150319_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roompricecategorytranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category Name'),
            preserve_default=True,
        ),
    ]
