from django.core.management.base import BaseCommand
from pathlib import Path
import os
from argparse import ArgumentParser
from typing import Any


class Command(BaseCommand):
    help: str = "Allows to create a custom command"

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "command_name", type=str, help="Command name you want to add"
        )

    def handle(self, *args: Any, **options: Any) -> None:
        command_name: str = options["command_name"].strip().lower()
        if not command_name:
            self.stdout.write(self.style.ERROR("Please enter command name"))
            return

        content: str = """from django.core.management.base import BaseCommand


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

        file_path: Path = Path(__file__).resolve().parent
        write_destination: Path = file_path / f"{command_name}.py"

        try:
            with open(write_destination, "w") as file:
                file.write(content)
            self.stdout.write(
                self.style.SUCCESS("Command created successfully")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error in creating command: {str(e)}")
            )
