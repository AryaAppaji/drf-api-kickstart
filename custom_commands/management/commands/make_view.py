from django.core.management.base import BaseCommand
from django.apps import apps
import os
from typing import Any


class Command(BaseCommand):
    help: str = "Allows to create a view"

    def handle(self, *args: Any, **options: Any) -> None:
        app_name: str = input("Enter the app name\n").strip()
        if not app_name:
            self.stdout.write(self.style.ERROR("Please provide app name"))
            return
        else:
            try:
                apps.get_app_config(app_name)
            except LookupError:
                self.stdout.write(
                    self.style.ERROR(f"App '{app_name}' not found.")
                )
                return

        view_name: str = input("Enter the view name\n").strip()
        if not view_name:
            self.stdout.write(self.style.ERROR("Please provide view name."))
            return

        view_path: str = os.path.join(app_name, f"views/{view_name}.py")

        if os.path.exists(view_path):
            self.stdout.write(self.style.ERROR("View already exists"))
            return

        content: str = """from django.shortcuts import render

# Create your views here.
"""

        try:
            with open(view_path, "w") as view_file:
                view_file.writelines(content)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to create view: {str(e)}")
            )
            return

        self.stdout.write(self.style.SUCCESS("View created successfully."))
