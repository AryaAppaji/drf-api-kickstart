from django.core.management.base import BaseCommand
from django.apps import apps
import os, sys


class Command(BaseCommand):
    help = "Adds a model to the given app"

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, help="Model name you want to add")
        parser.add_argument(
            "app_name", type=str, help="App name where you want to add the model"
        )
        parser.add_argument("table_name", type=str, help="Table name for the given model")

    def handle(self, *args, **kwargs):
        # Check if the required parameters are missing
        if not kwargs.get("model_name") or not kwargs.get("app_name") or not kwargs.get("table_name"):
            sys.stdout.write(
                self.style.ERROR("'model_name', 'app_name' and 'table_name' are required.")
            )
            return

        app_name = kwargs["app_name"]

        # Check if the app exists in the project
        try:
            apps.get_app_config(
                app_name
            )  # This will raise an exception if the app doesn't exist
        except LookupError:
            self.stdout.write(self.style.ERROR(f"App '{app_name}' not found."))
            return

        # Path to the models.py file
        model_file_path = os.path.join(app_name, "models.py")

        # Check if models.py exists
        if not os.path.exists(model_file_path):
            sys.stdout.write(
                self.style.ERROR(f"models.py file not found in app '{app_name}'.")
            )
            return

        # Read the models.py file and check for the import
        with open(model_file_path, "r") as file:
            lines = file.readlines()

        # Check if the 'from django.utils.timezone import now' is already present
        import_statement = "from django.utils.timezone import now"
        if not any(line.strip() == import_statement for line in lines):
            # Add the import at the beginning of the file
            lines.insert(0, f"{import_statement}\n")

        # Content to be added to models.py
        content = f"""
class {kwargs['model_name']}(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = now()  # Automatically update the field
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = "{kwargs['table_name']}"
        ordering = ['-created_at']
"""

        # Append the new model content to the file
        try:
            with open(model_file_path, "w") as file:
                file.writelines(lines)  # Write the lines back, including the import
                file.write(content)  # Add the new model at the end
            sys.stdout.write(
                self.style.SUCCESS(
                    f"Model '{kwargs['model_name']}' added to {model_file_path}."
                )
            )
        except Exception as e:
            sys.stdout.write(self.style.ERROR(f"Error adding model: {str(e)}"))
