import os
import unittest
import sys
import subprocess

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Option, Command

from app import app
from app.main import db
from app.main.model import user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOST = '0.0.0.0'
PORT = '80'

sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

# Originally from https://gist.github.com/menghan/9a632bbb0acb445f4f3a
class GunicornServer(Command):
    """Run the app within Gunicorn"""

    def get_options(self):
        from gunicorn.config import make_settings

        settings = make_settings()
        options = []

        for setting, klass in settings.items():
            if klass.cli:
                if klass.const is not None:
                    options.append(Option(*klass.cli, const=klass.const, action=klass.action))
                else:
                    options.append(Option(*klass.cli, action=klass.action))

        return options

    def run(self, *args, **kwargs):
        run_args = sys.argv[2:]
        run_args.append('-b '+HOST+':'+PORT)
        run_args.append('--reload')
        run_args.append('--log-level=debug')
        run_args.append('app:app')
        subprocess.Popen([os.path.join(os.path.dirname(sys.executable), 'gunicorn')] + run_args).wait()


manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', GunicornServer)

@manager.command
def run():
    app.run(host=HOST,port=PORT)

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
