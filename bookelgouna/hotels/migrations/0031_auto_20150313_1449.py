# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from uuslug import uuslug

from django.db import models, migrations


def generate_slugs(apps, schema_editor):
    Room = apps.get_model('hotels', 'Room')
    for room in Room.objects.filter(slug=''):
        slug = uuslug(room.title, start_no=2, instance=room, max_length=255, word_boundary=True)
        room.slug = slug
        room.save()


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0030_room_slug'),
    ]

    operations = [
        migrations.RunPython(generate_slugs, stub),
    ]
