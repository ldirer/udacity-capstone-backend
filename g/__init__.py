import json
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

app = Flask(__name__.split('.')[0])
app.config.from_object('g.config')

db = SQLAlchemy(app)


# DSN falls back to SENTRY_DSN environment variable.
sentry = Sentry(app, dsn='https://be91c746f73e41bd8a0c0ef3ee6f2bff:0e827d958fcc44ba8c3cc371a60bad90@sentry.io/109214',
                logging=True, level=logging.ERROR)

import g.api


# This works.
# app.logger.error("Test error.")


# For some reason when using --uwsgi-file only routes defined in THIS FILE are taken into account...
@app.route('/test_again')
def retest():
    return json.dumps({"hello": "world - 2!"})


# db.create_all()


if __name__ == '__main__':
    # The flask docs mention 'Python won't run this __init__ just fine', it seems we need a runserver file at a higher level but I'm not sure why.
    app.run(port=5000)

