from django.core.management.base import BaseCommand
from django.apps import apps
from django.core.management import call_command
from pathlib import Path
import shutil


class Command(BaseCommand):
    help = "Used to remove an existing app"

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name", type=str, help="App name you want to remove."
        )

    def handle(self, *args, **options):
        app_name = options["app_name"]

        # Check if app exists
        try:
            apps.get_app_config(app_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(f"App '{app_name}' not found."))
            return

        if app_name == "custom_commands":
            self.stdout.write(
                self.style.ERROR("You cannot remove the custom commands app")
            )
            return

        # Rollback migrations for the app
        call_command("migrate", app_name, "zero")

        # Get project root directory
        root_directory = Path(__file__).resolve().parent.parent.parent.parent

        # Create the app directory path
        app_directory = root_directory / app_name

        # List of settings files
        settings_files = [
            root_directory / "project" / "settings" / "local.py",
            root_directory / "project" / "settings" / "dev.py",
            root_directory / "project" / "settings" / "qa.py",
            root_directory / "project" / "settings" / "production.py",
        ]

        # Remove the app from settings files
        for settings_file in settings_files:
            if settings_file.exists():
                with settings_file.open("r") as file:
                    lines = file.readlines()
                with settings_file.open("w") as file:
                    for line in lines:
                        # Remove the app from the INSTALLED_APPS list
                        if app_name in line:
                            continue
                        file.write(line)

        # Remove the app directory recursively
        if app_directory.exists():
            try:
                shutil.rmtree(app_directory)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"App '{app_name}' and its contents successfully removed."
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error while removing app directory: {e}"
                    )
                )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"App directory '{app_directory}' does not exist."
                )
            )
