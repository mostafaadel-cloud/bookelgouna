# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20150403_0909'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Cart Item', 'verbose_name_plural': 'My trip'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Plan trip'},
        ),
        migrations.AlterField(
            model_name='cart',
            name='session_key',
            field=models.CharField(unique=True, max_length=40, verbose_name='Session key', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='content_type',
            field=models.ForeignKey(verbose_name='Content page', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='object_id',
            field=models.PositiveIntegerField(null=True, verbose_name='Related object'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='content_type',
            field=models.ForeignKey(verbose_name='Content page', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='object_id',
            field=models.PositiveIntegerField(null=True, verbose_name='Related object'),
            preserve_default=True,
        ),
    ]
