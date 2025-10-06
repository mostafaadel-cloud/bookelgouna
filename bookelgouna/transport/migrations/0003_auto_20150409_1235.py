# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0002_auto_20150409_1223'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transportcomment',
            unique_together=set([('entity', 'creator')]),
        ),
    ]
