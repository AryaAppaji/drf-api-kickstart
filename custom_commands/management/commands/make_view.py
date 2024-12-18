from django.core.management.base import BaseCommand
from pathlib import Path
from django.apps import apps
import os


class Command(BaseCommand):
    help = "Allows to create a view"

    def add_arguments(self, parser):
        # Add the arguments for your command here.
        """
        Example:
        parser.add_argument(
            "command_name", type=str, help="Command name you want to add"
        )
        """

    def handle(self, *args, **options):
        app_name = input("Enter the app name\n")
        if not app_name:
            self.stdout.write(self.style.ERROR("Please provide app name"))
        else:
            try:
                apps.get_app_config(app_name)
            except LookupError:
                self.stdout.write(self.style.ERROR(f"App '{app_name}' not found."))
                return

        view_name = input("Enter the view name\n")
        if not view_name:
            self.stdout.write(self.style.ERROR("Please provide view name."))

        view_path = os.path.join(app_name, f"views/{view_name}.py")

        if os.path.exists(view_path):
            self.stdout.write(self.style.ERROR("View already exists"))
            return
        content = """from django.shortcuts import render

# Create your views here.
"""

        try:
            with open(view_path, "w") as view:
                view.writelines(content)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create view."))
            return
        self.stdout.write(self.style.SUCCESS(f"View created successfully."))
