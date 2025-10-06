# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0032_auto_20150313_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Long Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='hotels.Room', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'hotels_room_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='roomtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.RemoveField(
            model_name='room',
            name='has_free_cancellation',
        ),
        migrations.RemoveField(
            model_name='room',
            name='is_breakfast_included',
        ),
        migrations.RemoveField(
            model_name='room',
            name='long_description',
        ),
        migrations.RemoveField(
            model_name='room',
            name='title',
        ),
    ]
