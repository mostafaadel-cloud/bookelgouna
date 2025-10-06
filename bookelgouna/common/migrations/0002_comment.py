# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object')),
                ('text', models.TextField(verbose_name='Text')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is approved')),
                ('content_type', models.ForeignKey(verbose_name='content page', blank=True, to='contenttypes.ContentType', null=True)),
                ('creator', models.ForeignKey(related_name='comments', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comment',
            },
            bases=(models.Model,),
        ),
    ]
