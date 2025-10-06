# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20150615_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'', verbose_name='Avatar', blank=True),
            preserve_default=True,
        ),
    ]
