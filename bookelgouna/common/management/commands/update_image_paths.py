# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models.loading import get_model


class Command(BaseCommand):
    help = "Updates all images paths in db."
    option_list = BaseCommand.option_list + (
        make_option('--dry-run', action='store_true', dest='dry_run', default=False,
            help="Just show what command would be made; don't actually do anything."),
    )
    args = "[app.model [app.model ...]]"

    def handle(self, *models, **options):
        """Updates all images paths in db for given models."""
        self.dry_run = options.get('dry_run', False)
        models = set(models)
        for model_name in models:
            mc = get_model(model_name)
            if mc is None:
                continue
            fields = []
            for field in mc._meta.fields:
                if field.get_internal_type() == 'FileField' or field.get_internal_type() == 'ImageField':
                    fields.append(field.name)

            if len(fields) > 0:
                messages = []
                files = mc.objects.all().values(*fields)
                for field2file_name in files:
                    for field, file_name in field2file_name.items():
                        if file_name.startswith('./'):
                            old_file_name = file_name
                            new_file_name = 'uploads' + file_name[1:]
                            messages.append(old_file_name + '\t->\t' + new_file_name)
                            if not self.dry_run:
                                mc.objects.filter(**{field: old_file_name}).update(**{field: new_file_name})
                if messages:
                    self.stdout.write('Model: ' + model_name)
                    for msg in messages:
                        self.stdout.write(msg)
                    self.stdout.write('-----------')

