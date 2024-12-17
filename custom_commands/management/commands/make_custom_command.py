from django.core.management.base import BaseCommand
from pathlib import Path
import os


class Command(BaseCommand):
    help = "Allows to create a custom command"

    def add_arguments(self, parser):
        parser.add_argument(
            "command_name", type=str, help="Command name you want to add"
        )

    def handle(self, *args, **options):
        if not options["command_name"]:
            self.stdout.write(self.style.ERROR("Please enter command name"))

        content = """from django.core.management.base import BaseCommand

        
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
"""

        file_path = Path(__file__).resolve().parent
        write_destination = os.path.join(file_path, options["command_name"] + ".py")

        try:
            with open(write_destination, "w") as file:
                file.write(content)
            self.stdout.write(self.style.SUCCESS(f"Command created successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error in creating command: {str(e)}"))
