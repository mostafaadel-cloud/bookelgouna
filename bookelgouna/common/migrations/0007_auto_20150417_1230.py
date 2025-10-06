# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_tempfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempfile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='File'),
            preserve_default=True,
        ),
    ]
