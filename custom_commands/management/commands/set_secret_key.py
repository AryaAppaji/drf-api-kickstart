from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from pathlib import Path


class Command(BaseCommand):
    help = "Generates and sets a random secret key in the .env file."

    def handle(self, *args, **options):
        try:
            env_path = Path(".env")
            secret_key = get_random_secret_key()

            if not env_path.exists():
                # Log an error and stop execution if the .env file does not exist
                self.stdout.write(
                    self.style.ERROR(
                        ".env file not found. Please create a .env file before running this command."
                    )
                )
                return

            # Read the existing .env file
            with open(env_path, "r") as env_file:
                env_content = env_file.readlines()

            # Update the DJANGO_SECRET_KEY line if it exists, or append it
            for i, line in enumerate(env_content):
                if line.startswith("DJANGO_SECRET_KEY"):
                    env_content[i] = (
                        f"DJANGO_SECRET_KEY='{secret_key}'\n"  # Overwrite the line
                    )
                    break
            else:
                env_content.append(
                    f"DJANGO_SECRET_KEY='{secret_key}'\n"
                )  # Add if not found

            # Write the updated content back to the .env file
            with open(env_path, "w") as env_file:
                env_file.writelines(env_content)

            self.stdout.write(
                self.style.SUCCESS("Secret key set successfully.")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Secret key setup failed: {str(e)}")
            )
