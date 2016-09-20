from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0])
app.config.from_object('g.config')

db = SQLAlchemy(app)

import g.api
import g.models

# db.create_all()


if __name__ == '__main__':
    # The flask docs mention 'Python won't run this __init__ just fine', it seems we need a runserver file at a higher level but I'm not sure why.
    app.run(port=5000)

