# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0051_auto_20150409_1223'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='hotelcomment',
            unique_together=set([('entity', 'creator')]),
        ),
    ]
