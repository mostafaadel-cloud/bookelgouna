# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
from django_countries import countries

def fill_countries(apps, schema_editor):
    Country = apps.get_model('users', 'Country')
    for code, name in countries:
        Country.objects.create(name=code)


def stub(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_preferred_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', django_countries.fields.CountryField(unique=True, max_length=2, verbose_name='Name')),
                ('default_language', models.CharField(default='en', max_length=2, choices=[('en', 'English'), ('ar', 'Arabic'), ('de', 'German'), ('ru', 'Russian'), ('it', 'Italian'), ('fr', 'French')])),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(fill_countries, stub),
    ]
