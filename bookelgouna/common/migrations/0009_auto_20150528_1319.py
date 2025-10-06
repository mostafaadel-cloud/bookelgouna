# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20150417_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempfile',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='File'),
            preserve_default=True,
        ),
    ]
