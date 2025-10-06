# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0055_remove_hotel_video_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Featured Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hotelimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
