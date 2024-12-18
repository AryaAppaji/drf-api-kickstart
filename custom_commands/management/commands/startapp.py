from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    help = "Create a new Django app with a custom structure and add it to all settings files"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="App name you want to create")

    def handle(self, *args, **options):
        app_name = options["app_name"]

        # Validate app name
        if not app_name.isalnum() and "_" not in app_name:
            self.stdout.write(
                self.style.ERROR(
                    "App name must contain only letters, numbers, and underscores."
                )
            )
            return

        if app_name.startswith("_") or app_name.endswith("_") or "_" == app_name:
            self.stdout.write(
                self.style.ERROR(
                    "App name cannot start, end with an underscore, or be only underscores."
                )
            )
            return

        # Get project root directory
        root_directory = Path(__file__).resolve().parent.parent.parent.parent

        # Create the app directory path
        app_directory = root_directory / app_name

        # Check if the app directory already exists
        if app_directory.exists():
            self.stdout.write(self.style.WARNING(f"App '{app_name}' already exists."))
            return

        # Create the app directory
        app_directory.mkdir(parents=True, exist_ok=False)

        # Content for admin.py
        admin_py_content = """from django.contrib import admin

# Register your models here.

"""

        # Create AppConfig name
        app_config_name = (
            "".join(word.capitalize() for word in app_name.split("_")) + "Config"
        )

        # Content for apps.py
        apps_py_content = f"""from django.apps import AppConfig

class {app_config_name}(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{app_name}"
"""

        # Content for models.py
        models_py_content = """from django.db import models

# Create your models here.

"""

        # Content for tests.py
        tests_py_content = """from django.test import TestCase

# Create your tests here.

"""

        # Files and their contents
        file_contents = {
            "__init__.py": "",
            "admin.py": admin_py_content,
            "apps.py": apps_py_content,
            "models.py": models_py_content,
            "tests.py": tests_py_content,
            "migrations/__init__.py": "",
            "services/__init__.py": "",
            "views/__init__.py": "",
        }

        # Create files and directories
        for filename, content in file_contents.items():
            file_path = app_directory / filename
            file_path.parent.mkdir(
                parents=True, exist_ok=True
            )  # Ensure parent directories exist
            with open(file_path, "w") as file:
                file.write(content)

        # Settings file paths
        settings_files = [
            root_directory / "project" / "settings" / "local.py",
            root_directory / "project" / "settings" / "dev.py",
            root_directory / "project" / "settings" / "qa.py",
            root_directory / "project" / "settings" / "production.py",
        ]

        # Add the app to INSTALLED_APPS in each settings file
        for settings_file in settings_files:
            try:
                if settings_file.exists():
                    with open(settings_file, "r") as file:
                        settings_content = file.readlines()

                    # Locate INSTALLED_APPS
                    installed_apps_index = None
                    for i, line in enumerate(settings_content):
                        if line.strip().startswith("INSTALLED_APPS"):
                            installed_apps_index = i
                            break

                    if installed_apps_index is not None:
                        # Find the end of the INSTALLED_APPS list
                        for j in range(installed_apps_index, len(settings_content)):
                            if settings_content[j].strip().endswith("]"):
                                # Check if app already exists
                                if f"    '{app_name}',\n" not in settings_content:
                                    settings_content.insert(j, f"    '{app_name}',\n")
                                break

                        # Write the updated settings back to the file
                        with open(settings_file, "w") as file:
                            file.writelines(settings_content)

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"'{app_name}' added to INSTALLED_APPS in {settings_file.name}."
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"INSTALLED_APPS not found in {settings_file.name}. Add the app manually."
                            )
                        )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Settings file {settings_file.name} not found."
                        )
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"An error occurred while updating {settings_file.name}: {str(e)}"
                    )
                )

        # Success message
        self.stdout.write(self.style.SUCCESS(f"'{app_name}' created successfully."))
