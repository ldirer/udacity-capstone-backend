import os

DEBUG = True

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                         'postgres://udacity:ezalojcsxou1239iipkz9"mffb@localhost/capstone')

SQLALCHEMY_ECHO = True
# Explicitely disable this to prevent a 'will be disabled by default' warning.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# A flag to make sure exceptions in resources are raised.
# By default they're just serialized and included in the response.
RESTLESS_DEBUG = True

microsoft_translator = {
    'CLIENT_ID': "udacity_capstone_belenos",
    'CLIENT_SECRET': "CKl0MFOE+62GJz/3MWSQWTk3lXJILCGBu056UwdSyv0="
}
