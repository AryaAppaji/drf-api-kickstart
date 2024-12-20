from django.core.management.base import BaseCommand
from pathlib import Path
from typing import Optional


class Command(BaseCommand):
    help: str = "Setup a view and its serializers for CRUD operations."

    def handle(self, *args: object, **options: object) -> None:
        view_name: str = input("Enter your view name:\n").strip().lower()

        if not view_name:
            self.stdout.write(self.style.ERROR("View name is required"))
            return

        if "_" not in view_name or not view_name.endswith("_view"):
            self.stdout.write(
                self.style.ERROR(
                    "View name should contain at least one underscore and should end with '_view'."
                )
            )
            return

        app_name: str = input("Enter your app name:\n").strip().lower()
        if not app_name:
            self.stdout.write(self.style.ERROR("App name is required"))
            return

        # Define root directory and paths
        root_directory: Path = (
            Path(__file__).resolve().parent.parent.parent.parent
        )
        app_directory: Path = root_directory / app_name
        view_path: Path = app_directory / "views" / f"{view_name}.py"
        serializer_path: Path = (
            app_directory
            / "serializers"
            / f"{view_name.replace('_view', '')}_serializer.py"
        )

        # Check if the app exists
        if not app_directory.exists():
            self.stdout.write(
                self.style.ERROR(f"App '{app_name}' does not exist.")
            )
            return

        # Check if the view already exists
        if view_path.exists():
            self.stdout.write(
                self.style.ERROR(f"View '{view_name}' already exists.")
            )
            return

        # Generate class names
        viewset_name: str = "".join(
            word.capitalize() for word in view_name.split("_")
        )
        class_name: str = viewset_name.replace("View", "")

        # Serializer content (generic placeholder)
        serializer_content: str = f"""from rest_framework import serializers


class {class_name}ListSerializer(serializers.BaseSerializer):
    pass


class Create{class_name}Serializer(serializers.BaseSerializer):
    pass


class Retrieve{class_name}Serializer(serializers.BaseSerializer):
    pass


class Update{class_name}Serializer(serializers.BaseSerializer):
    pass


class Destroy{class_name}Serializer(serializers.BaseSerializer):
    pass
"""

        # View content with serializer imports
        view_content: str = f"""from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Import serializers
from ..serializers.{view_name.replace('_view', '')}_serializer import (
    {class_name}ListSerializer,
    Create{class_name}Serializer,
    Retrieve{class_name}Serializer,
    Update{class_name}Serializer,
    Destroy{class_name}Serializer,
)


class {viewset_name}ViewSet(ViewSet):
    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk):
        pass

    def update(self, request):
        pass

    def destroy(self, request):
        pass
"""

        try:
            # Write the serializer file
            serializer_path.parent.mkdir(parents=True, exist_ok=True)
            with serializer_path.open("w") as serializer_file:
                serializer_file.write(serializer_content)

            # Write the view file
            view_path.parent.mkdir(parents=True, exist_ok=True)
            with view_path.open("w") as view_file:
                view_file.write(view_content)

            self.stdout.write(
                self.style.SUCCESS(
                    f"ViewSet and serializers for '{view_name}' created successfully."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Creation failed: {e}"))
