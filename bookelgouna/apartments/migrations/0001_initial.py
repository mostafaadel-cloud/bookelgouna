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
            name='Apartment',
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
                (b'cart_crop', image_cropping.fields.ImageRatioField('featured_image', '170x120', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cart crop')),
                ('type', models.PositiveSmallIntegerField(default=1, verbose_name='Status', choices=[(1, 'Apartment'), (2, 'Villa')])),
                ('number_of_rooms', models.PositiveSmallIntegerField(default=1, verbose_name='Number of rooms', validators=[django.core.validators.MinValueValidator(1)])),
                ('show_on_site', models.BooleanField(default=True, verbose_name='Show on site')),
            ],
            options={
                'verbose_name': 'Apartment',
                'verbose_name_plural': 'Apartments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentAmenity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Apartment Amenity',
                'verbose_name_plural': 'Apartment Amenities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentAmenityTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='apartments.ApartmentAmenity', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'apartments_apartmentamenity_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('language', models.CharField(default=b'en', max_length=15, verbose_name='Language', db_index=True, choices=[(b'en', b'English'), (b'ar', b'Arabic'), (b'de', b'German'), (b'ru', b'Russian'), (b'it', b'Italian'), (b'fr', b'French')])),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is approved')),
                ('creator', models.ForeignKey(related_name='apartment_comments', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('entity', models.ForeignKey(related_name='comments', verbose_name='Apartment', to='apartments.Apartment')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                (b'big_crop', image_cropping.fields.ImageRatioField('image', '1000x600', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='big crop')),
                (b'small_crop', image_cropping.fields.ImageRatioField('image', '138x135', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='small crop')),
                ('service', models.ForeignKey(related_name='images', verbose_name='Apartment', to='apartments.Apartment')),
            ],
            options={
                'verbose_name': 'Apartment Image',
                'verbose_name_plural': 'Apartment Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.IntegerField(verbose_name='Rate', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('reviewer', models.ForeignKey(related_name='apartment_reviews', verbose_name='Reviewer', to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(related_name='reviews', verbose_name='Apartment', to='apartments.Apartment')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ApartmentTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('long_description', models.TextField(verbose_name='Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='apartments.Apartment', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'apartments_apartment_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='apartmenttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='apartmentamenitytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='apartment',
            name='amenities',
            field=models.ManyToManyField(related_name='services', verbose_name='Amenities', to='apartments.ApartmentAmenity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apartment',
            name='duplicate',
            field=models.OneToOneField(related_name='origin', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='apartments.Apartment', verbose_name='Duplicate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(related_name='apartments', verbose_name='Owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ApprovedApartmentComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (approved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (approved)',
            },
            bases=('apartments.apartmentcomment',),
        ),
        migrations.CreateModel(
            name='UnapprovedApartment',
            fields=[
            ],
            options={
                'verbose_name': 'Apartment (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Apartments (unapproved)',
            },
            bases=('apartments.apartment',),
        ),
        migrations.CreateModel(
            name='UnapprovedApartmentComment',
            fields=[
            ],
            options={
                'verbose_name': 'Comment (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Comments (unapproved)',
            },
            bases=('apartments.apartmentcomment',),
        ),
    ]
