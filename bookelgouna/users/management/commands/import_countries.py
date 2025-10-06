from __future__ import unicode_literals
from django_countries import countries

from django.core.management.base import NoArgsCommand

from users.models import Country


class Command(NoArgsCommand):
    help = "Imports countries from django_countries app."

    def handle_noargs(self, **options):
        """Imports countries from django_countries app."""

        counter = 0
        for code, name in countries:
            country, created = Country.objects.get_or_create(name=code)
            if created:
                counter += 1
        if counter > 0:
            print 'Number of imported countries: %s.' % counter
        else:
            print 'No changes have been done.'
