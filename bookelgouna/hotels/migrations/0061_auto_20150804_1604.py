# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


MAX_ROOM_DESCRIPTION_LENGTH = 50


def shorten_room_type_name_field(apps, schema_editor):
    RoomType = apps.get_model('hotels', 'RoomType')
    for rt in RoomType.objects.all():
        for trans in rt.translations.all():
            name = trans.name
            if len(name) > MAX_ROOM_DESCRIPTION_LENGTH:
                trans.name = name[:MAX_ROOM_DESCRIPTION_LENGTH]
                trans.save()


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0060_auto_20150804_1401'),
    ]

    operations = [
        migrations.RunPython(shorten_room_type_name_field, stub),
        migrations.AlterField(
            model_name='roomtypetranslation',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='Name'),
            preserve_default=True,
        ),
    ]
