# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20150310_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(unique=True, max_length=255, verbose_name='Slug'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogposttranslation',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True, max_length=255, verbose_name='Slug'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='categorytranslation',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
