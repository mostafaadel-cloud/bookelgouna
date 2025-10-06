# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


def populate_price_categories_type(apps, schema_editor):
    Room = apps.get_model('hotels', 'Room')
    for room in Room.objects.all():
        room_type = room.type
        for pc in room.price_categories.all():
            pc.type = room_type
            pc.save()


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0057_auto_20150618_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='roompricecategory',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='hotels.RoomType', null=True),
            preserve_default=True,
        ),
        migrations.RunPython(populate_price_categories_type, stub),
        migrations.AlterField(
            model_name='roompricecategory',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='hotels.RoomType'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='room',
            name='type',
        ),
    ]
