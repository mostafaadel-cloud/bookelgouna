# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0054_auto_20150415_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='video_link',
        ),
    ]
