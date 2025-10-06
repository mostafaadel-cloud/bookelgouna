# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0005_auto_20150421_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Featured Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transportimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transportitem',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transportitemimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
