# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150311_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcomment',
            name='language',
            field=models.CharField(default=b'en', max_length=15, verbose_name='Language', db_index=True, choices=[(b'en', b'English'), (b'ar', b'Arabic'), (b'de', b'German'), (b'ru', b'Russian'), (b'it', b'Italian'), (b'fr', b'French')]),
            preserve_default=True,
        ),
    ]
