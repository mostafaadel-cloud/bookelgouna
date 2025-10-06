# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150109_0725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessownerinfo',
            name='user',
            field=models.OneToOneField(related_name='business_info', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=True,
        ),
    ]
