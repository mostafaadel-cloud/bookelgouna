# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.template.defaultfilters import slugify


def generate_slugs(apps, schema_editor):
    Hotel = apps.get_model('hotels', 'Hotel')
    for hotel in Hotel.objects.filter(slug=''):
        slug = slugify(hotel.title)
        hotel.slug = slug
        suffix = 2
        while Hotel.objects.filter(slug=hotel.slug).exists():
            hotel.slug = "%s-%d" % (slug, suffix)
            suffix += 1
        hotel.save()


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0025_hotel_slug'),
    ]

    operations = [
        migrations.RunPython(generate_slugs, stub),
    ]
