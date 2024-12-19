import os
from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = "Adds a model to the given app"

    def handle(self, *args, **kwargs):
        # Get inputs from the user
        model_name = input("Enter Model Name: ").strip()
        app_name = input("Enter App Name: ").strip()
        table_name = input("Enter Table Name: ").strip()

        # Check if the required parameters are missing
        if not model_name or not app_name or not table_name:
            self.stdout.write(
                self.style.ERROR(
                    "'model_name', 'app_name', and 'table_name' are required."
                )
            )
            return

        # Check if the app exists in the project
        try:
            apps.get_app_config(app_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(f"App '{app_name}' not found."))
            return

        # Path to the models.py file
        model_file_path = os.path.join(app_name, "models.py")

        # Check if models.py exists
        if not os.path.exists(model_file_path):
            self.stdout.write(
                self.style.ERROR(
                    f"models.py file not found in app '{app_name}'."
                )
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
        model_content = f"""
class {model_name}(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = now()  # Automatically update the field
        super().save(*args, **kwargs)

    class Meta:
        db_table = "{table_name}"
        ordering = ['-created_at']
"""

        # Append the new model content to the file
        try:
            with open(model_file_path, "w") as file:
                file.writelines(
                    lines
                )  # Write the lines back, including the import
                file.write(model_content)  # Add the new model at the end
            self.stdout.write(
                self.style.SUCCESS(
                    f"Model '{model_name}' added successfully to {model_file_path}."
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error adding model: {str(e)}")
            )
