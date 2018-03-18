from flask import current_app as app
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required

from PIL import Image

from project.server import bcrypt, db
from project.server.imagery import image_gps, image_recog
from project.server.models import Picture, User
from project.server.user.forms import LoginForm, RegisterForm

from werkzeug.utils import secure_filename

import os
import uuid

ALLOWED_UPLOAD_EXTENSIONS = set(['jpg','jpeg','png','gif'])

imagery_blueprint = Blueprint('imagery', __name__,)


def is_allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


def get_nearest_park_id(location):
    # TODO
    return 1


@imagery_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part.', 'error')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file.', 'error')
            return redirect(request.url)
        if file and is_allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            file_extension = original_filename.split('.')[-1]
            filename = str(uuid.uuid4()) + '.' + file_extension
            save_loc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_loc)
            location = image_gps.get_lat_lon(Image.open(save_loc))
            if location is None:
                flash('Images must have EXIF location data.', 'error')
                try:
                    os.remove(save_loc)
                except:
                    pass # suppress exceptions
                return redirect(request.url)
            else:
                # TODO add some logic to make park field the nearest park
                pass
            if ('localhost' in request.base_url or '127.0.0.1' in request.base_url):
                tags = '["test_tag1","test_tag2"]'
            else:
                available_url = request.base_url.replace('upload', 'img/') + filename
                tags = image_recog.get_tags_for_image(available_url)
            filesize = os.path.getsize(save_loc)
            park_id = get_nearest_park_id(location)
            picture = Picture(
                owner_id=current_user.get_id(),
                filename=filename,
                filesize=filesize,  # in the future we may scale down files, thus the 2 fields
                original_filename=original_filename,
                original_filesize=filesize,
                geolocation=location,
                tags=tags,
                park_id=park_id
            )
            db.session.add(picture)
            db.session.commit()
            flash('Upload successful.', 'success')
            return redirect(url_for('imagery.my_pictures'))
    # here it's a GET and we render the template
    return render_template('imagery/upload.html', is_authenticated=current_user.is_authenticated)


@imagery_blueprint.route('/img/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@imagery_blueprint.route('/mypics')
@login_required
def my_pictures():
    pictures = current_user.get_my_pictures()
    return render_template('imagery/mypics.html', pictures=pictures, is_authenticated=current_user.is_authenticated)
