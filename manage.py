# manage.py


from flask.cli import FlaskGroup

from project.server import create_app, db
from project.server.models import Park, User

import csv
import coverage
import os
import unittest

app = create_app()
cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', password='admin', admin=True))
    db.session.commit()


@cli.command()
def create_data():
    """Creates sample data, loads initial data."""
    field_names = ['latitude','longitude','info_string','name_abbr','name','state']
    csv_filenames = []
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            csv_filenames.append(os.path.join('data', file))
    for csv_filename in csv_filenames:
        with open(csv_filename, newline='', fieldnames=field_names) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Park(latitude=row['latitude'],
                         longitude=row['longitude'],
                         info_string=row['info_string'],
                         name_abbr=row['name_abbr'],
                         name=row['name'],
                         state=row['state'])
                db.session.add(p)
    db.session.commit()


@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1



if __name__ == '__main__':
    cli()
