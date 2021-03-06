import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
database_name = ""
pg_user = ""
pg_pass = ""
database_path = "postgresql://{}:{}@{}/{}".format(pg_user, pg_pass,'localhost:5432', database_name)


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_TRACK_MODIFICATIONS = False