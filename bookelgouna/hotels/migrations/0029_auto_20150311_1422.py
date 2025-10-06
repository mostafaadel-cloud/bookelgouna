# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0028_auto_20150311_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Long Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='hotels.Hotel', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'hotels_hotel_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='hoteltranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='long_description',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='title',
        ),
    ]
