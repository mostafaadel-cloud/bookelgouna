# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import django.db.models.deletion
from django.conf import settings
import image_cropping.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'On moderation'), (1, 'Approved'), (2, 'Rejected'), (3, 'Updating')])),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('review_num', models.IntegerField(default=0, verbose_name='Review Number')),
                ('review_avg', models.FloatField(default=0.0, verbose_name='Review Average')),
                ('address', models.CharField(max_length=255, verbose_name='Address', blank=True)),
                ('featured_image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Featured Image')),
                (b'big_crop', image_cropping.fields.ImageRatioField('featured_image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='big crop')),
                (b'small_crop', image_cropping.fields.ImageRatioField('featured_image', '138x135', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='small crop')),
                ('duplicate', models.OneToOneField(related_name='origin', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sports.Sport', verbose_name='Duplicate')),
                ('owner', models.ForeignKey(related_name='sports', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sport',
                'verbose_name_plural': 'SPORTS',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('language', models.CharField(default='en', max_length=15, verbose_name='Language', db_index=True, choices=[(b'en', b'English'), (b'ar', b'Arabic'), (b'de', b'German'), (b'ru', b'Russian'), (b'it', b'Italian'), (b'fr', b'French')])),
                ('is_approved', models.BooleanField(default=False, verbose_name='is approved')),
                ('creator', models.ForeignKey(related_name='sport_comments', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('entity', models.ForeignKey(related_name='comments', verbose_name='Sport', to='sports.Sport')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                (b'big_crop', image_cropping.fields.ImageRatioField('image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='big crop')),
                (b'small_crop', image_cropping.fields.ImageRatioField('image', '138x135', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='small crop')),
                ('service', models.ForeignKey(related_name='images', verbose_name='Sport', to='sports.Sport')),
            ],
            options={
                'verbose_name': 'Sport Image',
                'verbose_name_plural': 'Sport Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('type', models.PositiveSmallIntegerField(default=1, verbose_name='Type', choices=[(1, 'One Time'), (2, 'Subscription')])),
                ('featured_image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                (b'crop', image_cropping.fields.ImageRatioField('featured_image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop')),
                (b'cart_crop', image_cropping.fields.ImageRatioField('featured_image', '170x120', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cart crop')),
                ('price', models.FloatField(verbose_name='Price', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('number', models.PositiveSmallIntegerField(default=1, verbose_name='Number')),
                ('show_on_site', models.BooleanField(default=True, verbose_name='Show on site')),
                ('service', models.ForeignKey(related_name='items', verbose_name='Sport', to='sports.Sport')),
            ],
            options={
                'verbose_name': 'Sport Item',
                'verbose_name_plural': 'Sport Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                (b'crop', image_cropping.fields.ImageRatioField('image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop')),
                ('service', models.ForeignKey(related_name='images', verbose_name='Sport Item', to='sports.SportItem')),
            ],
            options={
                'verbose_name': 'Sport Item Image',
                'verbose_name_plural': 'Sport Item Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportItemTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='sports.SportItem', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'sports_sportitem_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.IntegerField(verbose_name='Rate', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('reviewer', models.ForeignKey(related_name='sport_reviews', verbose_name='Reviewer', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(related_name='reviews', verbose_name='Sport', to='sports.Sport')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SportTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='sports.Sport', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'sports_sport_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sporttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='sportreview',
            unique_together=set([('service', 'reviewer')]),
        ),
        migrations.AlterUniqueTogether(
            name='sportitemtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='sportcomment',
            unique_together=set([('entity', 'creator')]),
        ),
        migrations.CreateModel(
            name='ApprovedSportComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (approved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (approved)',
            },
            bases=('sports.sportcomment',),
        ),
        migrations.CreateModel(
            name='UnapprovedSport',
            fields=[
            ],
            options={
                'verbose_name': 'Sport (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Sports (unapproved)',
            },
            bases=('sports.sport',),
        ),
        migrations.CreateModel(
            name='UnapprovedSportComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (unapproved)',
            },
            bases=('sports.sportcomment',),
        ),
    ]
