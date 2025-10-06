# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields



class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookingEmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_type', models.IntegerField(verbose_name='Email type', choices=[(1, 'notify owner about new booking'), (2, 'notify owner about booking approval'), (3, 'notify tourist about booking approval'), (4, 'notify owner about booking manual reject'), (5, 'notify tourist about booking manual reject'), (6, 'notify owner about booking auto reject'), (7, 'notify tourist about booking auto reject'), (8, 'notify owner about noshow used'), (9, 'notify tourist about noshow used'), (10, 'notify owner about noshow cancellation'), (11, 'notify tourist about noshow cancellation')])),
            ],
            options={
                'verbose_name': 'Booking Email Template',
                'verbose_name_plural': 'Booking Email Templates',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookingEmailTemplateTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(help_text='You can use here these tags (these values will taken from recipient of this letter):<br>[EMAIL] - recipient email<br>[LOGIN] - recipient login<br>[FIRST_NAME] - recipient first name<br>[LAST_NAME] - recipient last name', max_length=255, verbose_name='Subject')),
                ('email_body', ckeditor.fields.RichTextField(help_text='You can use here these tags in every email:<br>[RECIPIENT_EMAIL] - recipient email<br>[RECIPIENT_LOGIN] - recipient login<br>[RECIPIENT_FIRST_NAME] - recipient first name<br>[RECIPIENT_LAST_NAME] - recipient last name<br>[ORDER_ITEM_PK] - booking unique identifier<br>[DATES] - booking dates<br>[BOOKINGS_LINK] - correct link to bookings for email recipient<br>[ITEM_DESCRIPTION] - item description depended from item<br>[QUANTITY] - number of items in booking (equals 1 for apartments and item-based productions)<br>[PRICE] - total price of this booking (quantity * price per item)<br>All emails to business owners can contain also:<br>[TOURIST_PK] - tourist unique identifier<br>Email to owner about booking approval can also contain:<br>[TOURIST_EMAIL] - tourist email<br>[TOURIST_PHONE] - tourist phone<br>Email to tourist about booking approval can also contain:<br>[OWNER_EMAIL] - owner email<br>[OWNER_PHONE] - owner phone<br>Email about owner inactivity can also contain:<br>[HOURS_OF_INACTIVITY] - owner was inactive during this number of hours so the booking was rejected', verbose_name='Email body')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='email_templates.BookingEmailTemplate', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'email_templates_bookingemailtemplate_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='bookingemailtemplatetranslation',
            unique_together=set([('language_code', 'master')]),
        )
    ]
