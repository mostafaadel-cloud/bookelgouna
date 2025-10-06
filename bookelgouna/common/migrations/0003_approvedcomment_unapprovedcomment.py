# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (approved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (approved)',
            },
            bases=('common.comment',),
        ),
        migrations.CreateModel(
            name='UnapprovedComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (unapproved)',
            },
            bases=('common.comment',),
        ),
    ]
