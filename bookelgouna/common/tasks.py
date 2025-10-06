# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from celery.task import periodic_task
from datetime import timedelta

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

from .models import TempFile


@periodic_task(run_every=timedelta(hours=24))
def remove_unused_images():
    # 1. delete old TempFile objects
    limit = timezone.now() - timedelta(hours=settings.TEMP_IMAGE_SHOULD_BE_DELETED_AFTER_HOURS)
    for tmpfile in TempFile.objects.filter(created__lte=limit):
        tmpfile.delete()
    # 2. delete orphaned images
    call_command('deleteorphaned')
    # 3. clear easy_thumbnails
    call_command('thumbnail_cleanup')
