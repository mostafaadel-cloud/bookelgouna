# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_auto_20150115_1646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='hotel',
            new_name='service',
        ),
    ]
