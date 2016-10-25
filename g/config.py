import json
import os

DEBUG = True

UDACITY_ENV = os.environ.get("UDACITY_ENV", "DEVELOPMENT")

with open("g/secrets.json", "r") as f:
    secrets = json.load(f)

os.environ.update(secrets)
PRODUCTION = UDACITY_ENV == "PRODUCTION"

if PRODUCTION:
    SENTRY_DSN = os.environ.get("SENTRY_DSN")

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                         'postgres://udacity:ezalojcsxou1239iipkz9"mffb@localhost/capstone')

SQLALCHEMY_ECHO = False
# Explicitely disable this to prevent a 'will be disabled by default' warning.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# A flag to make sure exceptions in resources are raised.
# By default they're just serialized and included in the response.
RESTLESS_DEBUG = True

microsoft_translator = {
    'CLIENT_ID': "udacity_capstone_belenos",
    'CLIENT_SECRET': os.environ.get("MICROSOFT_CLIENT_SECRET")
}
