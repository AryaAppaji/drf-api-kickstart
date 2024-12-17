
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help=""

    def add_arguments(self, parser):
        # Add the arguments for your command here.
        '''
        Example:
        parser.add_argument(
            "command_name", type=str, help="Command name you want to add"
        )
        '''
        pass

    def handle(self, *args, **options):
        # Write your command logic here.
        pass
