import os
from flask.ext.script import Shell, Manager
from flask.ext.script.commands import Server
from flask.ext.migrate import Migrate, MigrateCommand

from g import app, db, models


manager = Manager(app)


def make_context():
    return {'app': app, 'db': db, 'models': models}

"""Included by default, we can customize options."""
# make_context is a useful argument to save typing many imports. By default only app is loaded.
manager.add_command("shell", Shell(make_context=make_context))
manager.add_command("runserver", Server())


migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), 'g/migrations'))
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
