# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotels', '0022_roomprice_generated'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is approved')),
                ('creator', models.ForeignKey(related_name='hotel_comments', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('entity', models.ForeignKey(related_name='comments', verbose_name='Hotel', to='hotels.Hotel')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApprovedHotelComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (approved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (approved)',
            },
            bases=('hotels.hotelcomment',),
        ),
        migrations.CreateModel(
            name='UnapprovedHotelComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (unapproved)',
            },
            bases=('hotels.hotelcomment',),
        ),
    ]
