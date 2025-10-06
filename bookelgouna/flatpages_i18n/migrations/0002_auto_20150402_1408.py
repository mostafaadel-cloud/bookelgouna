# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages_i18n', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flatpage',
            options={'ordering': ('order',), 'verbose_name': 'Flat Page', 'verbose_name_plural': 'Flat Pages'},
        ),
        migrations.AddField(
            model_name='flatpage',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
