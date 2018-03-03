# project/server/models.py


import datetime
import uuid

from flask import current_app

from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Picture(db.Model):

    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    upload_date = db.Column(db.DateTime, nullable=False)
    owner_id = db.Column(db.Integer, nullable=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
    filesize = db.Column(db.String(255), nullable=True)
    original_filename = db.Column(db.String(255), nullable=True)
    original_filesize = db.Column(db.String(255), nullable=True)
    geolocation = db.Column(db.String(255), nullable=True)
    park_name = db.Column(db.String(255), nullable=True)
    tags = db.Column(db.String(255), nullable=True)

    def __init__(self, owner_id=None, file_extension='.jpg', filesize=None, original_filename=None, \
                    original_filesize=None, geolocation=None, park_name=None, tags=None):
        self.upload_date = datetime.datetime.now()
        self.owner_id = owner_id
        self.filename = str(uuid.uuid4()) + file_extension
        self.filesize = filesize
        self.original_filename = original_filename
        self.original_filesize = original_filesize
        self.geolocation = geolocation
        self.park_name = park_name
        self.tags = tags

    def __repr__(self):
        return '<Picture {0}>'.format(self.filename)
