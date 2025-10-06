# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0046_auto_20150326_1154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotelamenity',
            options={'ordering': ('category__order',), 'verbose_name': 'Hotel Amenity', 'verbose_name_plural': 'Hotel Amenities'},
        ),
        migrations.AlterField(
            model_name='hotel',
            name='owner',
            field=models.ForeignKey(related_name='hotels', verbose_name='Owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hotelreview',
            name='reviewer',
            field=models.ForeignKey(related_name='hotel_reviews', verbose_name='Reviewer', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
