# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20150417_1230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tempfile',
            options={'ordering': ('-created',)},
        ),
    ]
