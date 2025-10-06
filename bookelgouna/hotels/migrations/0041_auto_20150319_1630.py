# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0040_auto_20150318_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='roompricecategorytranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Category Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hotel',
            name='featured_image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Featured Image'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image'),
            preserve_default=True,
        ),
    ]
