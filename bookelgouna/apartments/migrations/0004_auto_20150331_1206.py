# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0003_auto_20150331_1115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartmentpricecategory',
            old_name='apartment',
            new_name='item',
        ),
    ]
