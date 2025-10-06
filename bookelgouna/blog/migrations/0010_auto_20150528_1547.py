# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20150416_0800'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name=b'crop',
            field=image_cropping.fields.ImageRatioField(b'featured_image', '1000x400', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name=b'Crop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postimage',
            name=b'crop',
            field=image_cropping.fields.ImageRatioField(b'image', '1000x400', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name=b'Crop'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='featured_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'uploads', verbose_name='Featured Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=easy_thumbnails.fields.ThumbnailerImageField(help_text='add 18x18 image or bigger (then it will be cropped) otherwise default icon will be used', upload_to=b'uploads', verbose_name='Icon', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'uploads', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
