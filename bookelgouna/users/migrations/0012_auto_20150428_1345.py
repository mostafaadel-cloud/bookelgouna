# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_user_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessownerinfo',
            name='show_next_link',
            field=models.BooleanField(default=True, verbose_name='Show "Next" link in profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='businessownerinfo',
            name='service_type',
            field=models.PositiveSmallIntegerField(verbose_name='Service Type', choices=[(0, 'Hotel'), (1, 'Apartment'), (2, 'Transport'), (3, 'Excursion'), (4, 'Sport'), (5, 'Entertainment')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'avatar', '118x118', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='Cropping'),
            preserve_default=True,
        ),
    ]
