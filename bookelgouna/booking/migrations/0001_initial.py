# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_key', models.CharField(unique=True, max_length=40, verbose_name='session key', blank=True)),
                ('user', models.OneToOneField(related_name='cart', null=True, verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object')),
                ('from_date', models.DateField(verbose_name='From Date')),
                ('to_date', models.DateField(verbose_name='To Date')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity', choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('cart', models.ForeignKey(related_name='items', verbose_name='Cart', to='booking.Cart')),
                ('content_type', models.ForeignKey(verbose_name='content page', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.FloatField(default=0.0, verbose_name='Total Price', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('status', models.IntegerField(default=1, verbose_name='Status', choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Rejected')])),
                ('user', models.ForeignKey(related_name='orders', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, verbose_name='related object')),
                ('price', models.FloatField(default=0.0, verbose_name='Price', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('from_date', models.DateField(verbose_name='From Date')),
                ('to_date', models.DateField(verbose_name='To Date')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity', choices=[(1, 1), (2, 2), (3, 3), (4, 4)])),
                ('status', models.IntegerField(default=1, verbose_name='Status', choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Rejected')])),
                ('content_type', models.ForeignKey(verbose_name='content page', blank=True, to='contenttypes.ContentType', null=True)),
                ('order', models.ForeignKey(related_name='items', verbose_name='Order Item', to='booking.Order')),
                ('owner', models.ForeignKey(related_name='order_items', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Order Items',
            },
            bases=(models.Model,),
        ),
    ]
