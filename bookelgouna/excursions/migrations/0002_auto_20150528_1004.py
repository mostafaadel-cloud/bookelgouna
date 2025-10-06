# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursion',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Featured Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursionimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursionitem',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='excursionitemimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
