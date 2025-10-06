# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotels', '0020_auto_20150213_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.IntegerField(verbose_name='Rate', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('reviewer', models.ForeignKey(related_name='reviews', verbose_name='Reviewer', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(related_name='reviews', verbose_name='Hotel', to='hotels.Hotel')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hotel',
            name='review_avg',
            field=models.FloatField(default=0.0, verbose_name='Review Average'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotel',
            name='review_num',
            field=models.IntegerField(default=0, verbose_name='Review Number'),
            preserve_default=True,
        ),
    ]
