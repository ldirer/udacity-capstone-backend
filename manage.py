import os
from flask_script import Shell, Manager, prompt_bool
from flask_script.commands import Server
from flask_migrate import Migrate, MigrateCommand

from g import app, db, models


manager = Manager(app)


def make_context():
    return {'app': app, 'db': db, 'models': models}

"""Included by default, we can customize options."""
# make_context is a useful argument to save typing many imports. By default only app is loaded.
manager.add_command("shell", Shell(make_context=make_context))
manager.add_command("runserver", Server())


migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), 'g/migrations'))


@MigrateCommand.command
def create_db():
    """Create database tables from sqlalchemy models."""
    db.create_all()


@MigrateCommand.command
def drop():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()

manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
