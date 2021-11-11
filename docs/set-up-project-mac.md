# Run BikeMaps.org locally on a Mac

This doc summarizes how I set up Bikemaps.org on my local machine. It could eventually be moved to the readme but the instructions are pretty platform specific so I'd like to include alternative instructions for anything that wouldn't work on Windows or Linux.

## Install Python 3

<a href='https://docs.python-guide.org/starting/install3/osx/'>Instructions for a system install of Python 3 here</a>

I prefer using pyenv to manage python versions and am using 3.6.1 for this project. Using <a href='https://brew.sh/'>homebrew</a> to install:
``` bash
brew update
brew install pyenv
pyenv install 3.6.1
```
More docs on pyenv <a href='https://github.com/pyenv/pyenv#installation'>here</a>.


To see which python versions are downloaded and available to pyenv: `pyenv versions`

To switch versions: `pyenv global 3.6.1`

To see current python path: `which python`

## Set up virtual environment

It is advisable to run a python virtual environment for the BikeMaps.org project. This guarantees an isolated context for your python version and dependencies, which avoids issues with conflicts between this project and your other projects or your system.

venv is the newer version of virtualenv that ships with python3, so it doesn't need to be installed.

Virtual environments can be stored in their own directory separate from the projects they are associated with. To create one if it doesn't already exist:

`mkdir /Users/your-username/virtualenvs && cd $_`

Create and activate a new venv for the bikemaps project:
``` bash
python -m venv bikemaps_venv
. bikemaps_venv/bin/activate
```

Verify the environment has the correct python version: `python -V`

To exit the venv: `deactivate`

## Set up database

I've found the easiest way to run a PostgreSQL server is with <a href='https://postgresapp.com/'>Postgres.app</a>.

Once the server is running, create the bikemaps database with 'postgres' as the user:
``` bash
createdb -U postgres bikeDB
```

Verify you can connect to the database: `psql -U postgres -d bikeDB`

View tables: `\dt+`

Exit: `\q`

Postgres.app includes the postgis extension out of the box, but if necessary install with: `psql -U postgres -d bikeDB -c "CREATE EXTENSON postgis;"`

## Run Django project

From the BikeMaps project directory with the virtual environment activated, install the requirements with the most recent version of pip.
``` bash
pip install --upgrade pip
pip install -r requirements.txt
```

Generate and run migrations to add all database tables:
``` bash
./manage.py makemigrations
./manage.py migrate
```

Start the development server at 127.0.0.1:8000 and visit in a web browser.
``` bash
./manage.py runserver
```

Exit with ctrl-c.

To access the admin page, create a superuser account to log in with.
``` bash
./manage.py createsuperuser
```

## To do
verify exact python & postgres versions that should be used once server is upgraded to accommodate most recent bikemaps version (current docs say Postgres 9.3 and Python 2.7)
