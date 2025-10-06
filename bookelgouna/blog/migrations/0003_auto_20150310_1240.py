# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150305_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='video_id',
            field=models.CharField(max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='video_link',
            field=models.CharField(help_text='youtube video link like http://www.youtube.com/watch?v=_oPAwA_Udwc. do not use embeded youtube link here.', max_length=255, verbose_name='Video', blank=True),
            preserve_default=True,
        ),
    ]
