from django.core.management import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("rebuild_index", interactive=False, using=[lang[0] for lang in settings.LANGUAGES])