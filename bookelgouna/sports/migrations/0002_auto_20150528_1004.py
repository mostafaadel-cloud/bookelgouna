# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Featured Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sportimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sportitem',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sportitemimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='uploads', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
