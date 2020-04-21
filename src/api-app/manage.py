import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main.start import create_app, db

from app.main.model import category, user, sample, classification

#this is where the app gets setup and then gets installed
app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
