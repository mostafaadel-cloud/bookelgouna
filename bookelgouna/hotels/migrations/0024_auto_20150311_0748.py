# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0023_approvedhotelcomment_hotelcomment_unapprovedhotelcomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UnapprovedRoom',
        ),
        migrations.RemoveField(
            model_name='room',
            name='duplicate',
        ),
        migrations.RemoveField(
            model_name='room',
            name='status',
        ),
    ]
