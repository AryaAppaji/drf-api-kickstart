## Prerequisites.

To use this template you should have `Python 3.13` installed on your system and `uv` package to be installed. To install uv run the following command:

```bash
pip install uv
```

## Setup in your system.

- Create a new repository using the `Use this template` button in this repository.

- Next clone the repository into your local system.

- Copy the `.env.example` file and paste it in the same directory and rename it as `.env`.

- And create a database if your site uses database and set the following env variables:

  `DB_ENGINE` - databese engine you are using.

  `DB_HOST` - IP address where the databse hosted.

  `DB_PORT` - Port to connect the database server.

  `DB_NAME` - Name of the database you are using.

  `DB_USER` - Username of the database you are using.

  `DB_PASSWORD` - Password of the databse.

- Then run the following commands:

  ```bash
  uv sync
  ```

  This will install the default dependencies of the project.

  If you want to install a specific group of dependencies use

  ```bash
  uv sync --group=group_name
  ```

  And if you want to install dependencies from all groups use

  ```bash
  uv sync --all-groups
  ```

  And after that you have to set the secret key using the below command

  ```bash
  uv run set_secret_key
  ```

Now you can run all the commands prefix with uv like

```bash
uv run manage.py <command>
```

instead of

```bash
python manage.py <command>
```

And you are good to go.
