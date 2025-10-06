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
            name='Excursion',
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
                ('duplicate', models.OneToOneField(related_name='origin', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='excursions.Excursion', verbose_name='Duplicate')),
                ('owner', models.ForeignKey(related_name='excursions', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Excursion',
                'verbose_name_plural': 'Excursions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('language', models.CharField(default='en', max_length=15, verbose_name='Language', db_index=True, choices=[(b'en', b'English'), (b'ar', b'Arabic'), (b'de', b'German'), (b'ru', b'Russian'), (b'it', b'Italian'), (b'fr', b'French')])),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is approved')),
                ('creator', models.ForeignKey(related_name='excursion_comments', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('entity', models.ForeignKey(related_name='comments', verbose_name='Excursion', to='excursions.Excursion')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                (b'big_crop', image_cropping.fields.ImageRatioField('image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='big crop')),
                (b'small_crop', image_cropping.fields.ImageRatioField('image', '138x135', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='small crop')),
                ('service', models.ForeignKey(related_name='images', verbose_name='Excursion', to='excursions.Excursion')),
            ],
            options={
                'verbose_name': 'Excursion Image',
                'verbose_name_plural': 'Excursion Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('type', models.PositiveSmallIntegerField(default=1, verbose_name='Type', choices=[(1, 'One Time'), (2, 'Tour')])),
                ('featured_image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                (b'crop', image_cropping.fields.ImageRatioField('featured_image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop')),
                (b'cart_crop', image_cropping.fields.ImageRatioField('featured_image', '170x120', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cart crop')),
                ('price', models.FloatField(verbose_name='Price', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('number', models.PositiveSmallIntegerField(default=1, verbose_name='Number')),
                ('show_on_site', models.BooleanField(default=True, verbose_name='Show on site')),
                ('service', models.ForeignKey(related_name='items', verbose_name='Excursion', to='excursions.Excursion')),
            ],
            options={
                'verbose_name': 'Excursion Item',
                'verbose_name_plural': 'Excursion Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionItemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                (b'crop', image_cropping.fields.ImageRatioField('image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='crop')),
                ('service', models.ForeignKey(related_name='images', verbose_name='Excursion Item', to='excursions.ExcursionItem')),
            ],
            options={
                'verbose_name': 'Excursion Item Image',
                'verbose_name_plural': 'Excursion Item Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionItemTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='excursions.ExcursionItem', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'excursions_excursionitem_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.IntegerField(verbose_name='Rate', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('reviewer', models.ForeignKey(related_name='excursion_reviews', verbose_name='Reviewer', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(related_name='reviews', verbose_name='Excursion', to='excursions.Excursion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='excursions.Excursion', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'excursions_excursion_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='excursiontranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='excursionreview',
            unique_together=set([('service', 'reviewer')]),
        ),
        migrations.AlterUniqueTogether(
            name='excursionitemtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='excursioncomment',
            unique_together=set([('entity', 'creator')]),
        ),
        migrations.CreateModel(
            name='ApprovedExcursionComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (approved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (approved)',
            },
            bases=('excursions.excursioncomment',),
        ),
        migrations.CreateModel(
            name='UnapprovedExcursion',
            fields=[
            ],
            options={
                'verbose_name': 'Excursion (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Excursions (unapproved)',
            },
            bases=('excursions.excursion',),
        ),
        migrations.CreateModel(
            name='UnapprovedExcursionComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (unapproved)',
            },
            bases=('excursions.excursioncomment',),
        ),
    ]
