# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0008_auto_20150409_1223'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='apartmentcomment',
            unique_together=set([('entity', 'creator')]),
        ),
    ]
