# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is approved')),
                ('creator', models.ForeignKey(related_name='post_comments', verbose_name='Creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Blog Comment',
                'verbose_name_plural': 'Blog Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('featured_image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Featured Image')),
                ('video_link', models.CharField(max_length=255, verbose_name='Video', blank=True)),
                ('slug', models.SlugField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogPostTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Long Description')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='blog.BlogPost', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'blog_blogpost_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('icon', sorl.thumbnail.fields.ImageField(help_text='add 18x18 image or bigger (then it will be cropped) otherwise default icon will be used', upload_to=b'', verbose_name='Icon', blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='blog.Category', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'blog_category_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageField(upload_to=b'', verbose_name='Image')),
                ('post', models.ForeignKey(related_name='images', verbose_name='Post', to='blog.BlogPost')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='blogposttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.ForeignKey(related_name='posts', verbose_name='Category', to='blog.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogcomment',
            name='post',
            field=models.ForeignKey(related_name='comments', verbose_name='Post', to='blog.BlogPost'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='ApprovedBlogComment',
            fields=[
            ],
            options={
                'verbose_name': 'Blog Comment (approved)',
                'proxy': True,
                'verbose_name_plural': 'Blog Comments (approved)',
            },
            bases=('blog.blogcomment',),
        ),
        migrations.CreateModel(
            name='UnapprovedBlogComment',
            fields=[
            ],
            options={
                'verbose_name': 'Blog Comment (unapproved)',
                'proxy': True,
                'verbose_name_plural': 'Blog Comments (unapproved)',
            },
            bases=('blog.blogcomment',),
        ),
    ]
