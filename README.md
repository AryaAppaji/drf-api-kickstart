# Django Project Template

This repository serves as a template for setting up Django projects quickly and easily. It includes essential configuration and packages to streamline the development of common backend features. Ideal for developers looking for a reliable starting point, this template supports multiple databases, external storage integration, and real-time WebSocket communication.

## Features

- **Multi-Environment Setup**  
  Pre-configured settings for development, staging, and production environments, allowing you to switch between them effortlessly by adjusting environment variables.

- **Database Support**  
  Packages included for the following databases:

  - MySQL
  - PostgreSQL
  - MSSQL
  - MariaDB
  - MongoDB
  - OracleDB

- **Django REST Framework (DRF)**  
  A pre-configured setup for building RESTful APIs using DRF, saving time on setup and integration.

- **Django-Storages Integration**  
  Seamless integration with `django-storages` for easy communication with external storage systems, such as Amazon S3.

- **WebSocket Support (Channels)**  
  Real-time communication capabilities through WebSocket support via Django Channels.

- **Pre-built custom-commands for faster development**
  `add_model` - Adds the basic sacaffold for given model name to the given app.

  `make_custom_command` - Adds the boilerplate to create a custom command.

  `make_view` - Adds the boilerplate to create a view file in given app.

  `removeapp` - Removes the given app from the project.

  `set_secret_key` - Creates the secret key for the selected environment and adds it to the `.env` file.

  `setup_crud_view` - Creates a view for the CRUD operations along with their serializers under the given app.

  `startapp` - Customized the built-in startapp command to include additional directories and add the newly created app to the settings file.

  To know how to use this template see [SETUP.md](SETUP.md)

## Acknowledgments

Parts of this project are inspired by the [HackSoft Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example), which is licensed under the MIT License.
