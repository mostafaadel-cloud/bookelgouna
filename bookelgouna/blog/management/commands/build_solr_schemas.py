from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        raise ImproperlyConfigured("This command is not yet done.")