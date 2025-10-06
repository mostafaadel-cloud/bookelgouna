# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150409_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogposttranslation',
            name='desc_metatag',
            field=models.CharField(default='description metatag stub', help_text='max length is 160 letters', max_length=160, verbose_name='description metatag'),
            preserve_default=False,
        ),
    ]
