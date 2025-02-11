from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    help = "Create a new Django app with a custom structure and add it to all settings files."

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name", type=str, help="Name of the app you want to create."
        )

    def handle(self, *args, **options):
        app_name: str = options["app_name"]

        # Validate app name
        if not app_name.isidentifier():
            self.stdout.write(
                self.style.ERROR(
                    "Invalid app name. It must contain only letters, numbers, and underscores, and cannot start with a number."
                )
            )
            return

        # Get project root directory
        root_directory = Path(__file__).resolve().parent.parent.parent.parent

        # Create the app directory path
        app_directory = root_directory / app_name

        # Check if the app directory already exists
        if app_directory.exists():
            self.stdout.write(
                self.style.WARNING(f"App '{app_name}' already exists.")
            )
            return

        # Create the app directory
        app_directory.mkdir(parents=True, exist_ok=False)

        # Define content for app files
        file_templates: dict = {
            "__init__.py": "",
            "admin.py": "from django.contrib import admin\n\n# Register your models here.\n",
            "apps.py": f"""from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{app_name}"
""",
            "models.py": "from django.db import models\n\n# Create your models here.\n",
            "tests.py": "from django.test import TestCase\n\n# Create your tests here.\n",
            "views/__init__.py": "",
            "serializers/__init__.py": "",
            "services/__init__.py": "",
            "migrations/__init__.py": "",
        }

        # Generate files and directories
        for relative_path, content in file_templates.items():
            file_path = app_directory / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open("w") as file:
                file.write(content)

        self.stdout.write(
            self.style.SUCCESS(
                f"App '{app_name}' structure created successfully."
            )
        )

        # Settings file paths
        settings_files: list[Path] = [
            root_directory / "project" / "settings" / "local.py",
            root_directory / "project" / "settings" / "dev.py",
            root_directory / "project" / "settings" / "qa.py",
            root_directory / "project" / "settings" / "production.py",
        ]

        # Add app to INSTALLED_APPS in settings files
        for settings_file in settings_files:
            if not settings_file.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f"Settings file '{settings_file.name}' not found."
                    )
                )
                continue

            try:
                with settings_file.open("r") as file:
                    settings_content = file.readlines()

                # Locate the INSTALLED_APPS block
                try:
                    start_index = next(
                        i
                        for i, line in enumerate(settings_content)
                        if "INSTALLED_APPS" in line
                    )
                    end_index = next(
                        i
                        for i in range(start_index, len(settings_content))
                        if settings_content[i].strip().endswith("]")
                    )

                    # Check if app is already in INSTALLED_APPS
                    if (
                        f"    '{app_name}',\n"
                        not in settings_content[start_index:end_index]
                    ):
                        settings_content.insert(
                            end_index, f"    '{app_name}',\n"
                        )
                        with settings_file.open("w") as file:
                            file.writelines(settings_content)
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Added '{app_name}' to INSTALLED_APPS in '{settings_file.name}'."
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"'{app_name}' is already present in INSTALLED_APPS in '{settings_file.name}'."
                            )
                        )
                except StopIteration:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Could not locate INSTALLED_APPS in '{settings_file.name}'. Add the app manually."
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error updating '{settings_file.name}': {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"App '{app_name}' setup completed.")
        )
