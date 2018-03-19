# project/server/models.py


import datetime

from flask import current_app as app

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
            password, app.config.get('BCRYPT_LOG_ROUNDS')
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

    def get_my_pictures(self):
        my_pictures = Picture.query.filter_by(owner_id=self.id).order_by(Picture.upload_date.desc()).all()
        return my_pictures

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
    park_id = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.String(255), nullable=True)

    def __init__(self, filename, owner_id=None, filesize=None, original_filename=None, \
                    original_filesize=None, geolocation=None, park_id=None, tags=None):
        self.upload_date = datetime.datetime.now()
        self.owner_id = owner_id
        self.filename = filename
        self.filesize = filesize
        self.original_filename = original_filename
        self.original_filesize = original_filesize
        self.geolocation = geolocation
        self.park_id = park_id
        self.tags = tags

    def get_caption(self):
        if self.original_filename is not None:
            return self.original_filename
        elif self.upload_date is not None:
            return str(self.upload_date)
        else:
            return 'Picture'

    def get_details_url(self):
        return app.config.get('BASE_URL') + '/image-details/' + str(self.id)

    def get_file_url(self):
        return app.config.get('BASE_URL') + '/img/' + self.filename

    def __repr__(self):
        return '<Picture {0}>'.format(self.filename)

class Park(db.Model):

    __tablename__ = 'parks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.String(128), nullable=True)
    longitude = db.Column(db.String(128), nullable=True)
    info_string = db.Column(db.String(512), nullable=True)
    name_abbr = db.Column(db.String(128), nullable=True)
    name = db.Column(db.String(128), nullable=True)
    state = db.Column(db.String(128), nullable=True)

    def __init__(self, latitude=0.0, longitude=0.0, info_string=None, \
                    name_abbr=None, name=None, state=None):
        self.latitude = latitude
        self.longitude = longitude
        self.info_string = info_string
        self.name_abbr = name_abbr
        self.name = name
        self.state = state

    def get_id(self):
        return self.id

    def get_lat_float(self):
        return float(self.latitude)

    def get_lon_float(self):
        return float(self.longitude)

    def __repr__(self):
        return '<Park {0}>'.format(self.id)
