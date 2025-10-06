# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0036_auto_20150316_1103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mealplan',
            options={'verbose_name': 'Meal Plan', 'verbose_name_plural': 'Meal Plans'},
        ),
        migrations.AlterModelOptions(
            name='roomprice',
            options={'verbose_name': 'Room Price', 'verbose_name_plural': 'Room Prices'},
        ),
        migrations.AlterModelOptions(
            name='roompricecategory',
            options={'verbose_name': 'Room Price Category', 'verbose_name_plural': 'Room Price Categories'},
        ),
    ]
