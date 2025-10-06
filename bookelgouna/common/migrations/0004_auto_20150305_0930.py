# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_approvedcomment_unapprovedcomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApprovedComment',
        ),
        migrations.DeleteModel(
            name='UnapprovedComment',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
