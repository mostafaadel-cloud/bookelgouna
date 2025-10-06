# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogcomment_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='is approved'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='video_link',
            field=models.CharField(help_text='YouTube video link like: \nhttp://www.youtube.com/watch?v=_oPAwA_Udwc\nDo not use embedded YouTube link here.', max_length=255, verbose_name='Video', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=sorl.thumbnail.fields.ImageField(help_text='Add 18x18 image or bigger (and it will be cropped). Otherwise, default icon will be used.', upload_to=b'', verbose_name='Icon', blank=True),
            preserve_default=True,
        ),
    ]
