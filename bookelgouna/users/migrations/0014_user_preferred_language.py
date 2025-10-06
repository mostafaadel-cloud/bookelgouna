# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20150515_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='preferred_language',
            field=models.CharField(default='en', max_length=2, verbose_name='Language', choices=[('en', 'English'), ('ar', 'Arabic'), ('de', 'German'), ('ru', 'Russian'), ('it', 'Italian'), ('fr', 'French')]),
            preserve_default=True,
        ),
    ]
