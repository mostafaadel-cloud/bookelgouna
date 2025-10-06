# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

MAX_ROOM_DESCRIPTION_LENGTH = 50


def shorten_room_description_field(apps, schema_editor):
    Room = apps.get_model('hotels', 'Room')
    for room in Room.objects.all():
        for trans in room.translations.all():
            desc = trans.long_description
            if len(desc) > MAX_ROOM_DESCRIPTION_LENGTH:
                trans.long_description = desc[:MAX_ROOM_DESCRIPTION_LENGTH]
                trans.save()


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0058_auto_20150804_1254'),
    ]

    operations = [
        migrations.RunPython(shorten_room_description_field, stub),
        migrations.AlterField(
            model_name='roomtranslation',
            name='long_description',
            field=models.CharField(max_length=50, verbose_name='Long Description'),
            preserve_default=True,
        ),
    ]
