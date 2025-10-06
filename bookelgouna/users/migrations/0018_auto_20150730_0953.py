# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20150716_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Avatar', blank=True),
            preserve_default=True,
        ),
    ]
