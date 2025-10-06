# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvedblogcomment',
            options={'verbose_name': 'Comment (approved)', 'verbose_name_plural': 'Comments (approved)'},
        ),
        migrations.AlterModelOptions(
            name='blogcomment',
            options={'ordering': ('-created',), 'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
        migrations.AlterModelOptions(
            name='unapprovedblogcomment',
            options={'verbose_name': 'Comment (unapproved)', 'verbose_name_plural': 'Comments (unapproved)'},
        ),
        migrations.RenameField(
            model_name='blogcomment',
            old_name='post',
            new_name='entity',
        ),
    ]
