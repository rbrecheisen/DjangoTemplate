from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import LogOutputModel


class Command(BaseCommand):
    help = 'Clears logs'

    def handle(self, *args, **kwargs):
        LogOutputModel.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted logs'))