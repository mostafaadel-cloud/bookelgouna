# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_set_site_domain_and_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=100, verbose_name='URL', db_index=True)),
                ('template_name', models.CharField(help_text="Example: 'flatpages_i18n/contact_page.html'. If this isn't provided, the system will use 'flatpages_i18n/default.html'.", max_length=70, verbose_name='template name', blank=True)),
                ('registration_required', models.BooleanField(default=False, help_text='If this is checked, only logged-in users will be able to view the page.', verbose_name='registration required')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('is_published', models.BooleanField(default=True, verbose_name='is published')),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
            options={
                'ordering': ('url',),
                'verbose_name': 'Flat Page',
                'verbose_name_plural': 'Flat Pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlatPageTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('content', ckeditor.fields.RichTextField(verbose_name='content')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='flatpages_i18n.FlatPage', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'flatpages_i18n_flatpage_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='flatpagetranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
