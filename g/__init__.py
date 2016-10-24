import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0])
app.config.from_object('g.config')

db = SQLAlchemy(app)

import g.api


# For some reason when using --uwsgi-file only routes defined in THIS FILE are taken into account...
@app.route('/test_again')
def retest():
    return json.dumps({"hello": "world - 2!"})


# db.create_all()


if __name__ == '__main__':
    # The flask docs mention 'Python won't run this __init__ just fine', it seems we need a runserver file at a higher level but I'm not sure why.
    app.run(port=5000)

