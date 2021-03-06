from flask import current_app as app
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, send_from_directory
from flask_login import current_user, login_user, \
    logout_user, login_required

from math import atan2, cos, pi, sin, sqrt

from PIL import Image

from project.server import bcrypt, db
from project.server.imagery import image_gps, image_recog
from project.server.models import Park, Picture, User
from project.server.user.forms import LoginForm, RegisterForm

from werkzeug.utils import secure_filename

import os
import random
import uuid

ALLOWED_UPLOAD_EXTENSIONS = set(['jpg','jpeg','png','gif'])

imagery_blueprint = Blueprint('imagery', __name__,)


def is_allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


def deg_to_rad(deg):
    return deg * (pi / 180)


def get_distance_in_km(lat1, lon1, lat2, lon2):
    r = 6371  # radius of earth in km
    dlat = deg_to_rad(lat2 - lat1)
    dlon = deg_to_rad(lon2 - lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(deg_to_rad(lat1)) \
                * cos(deg_to_rad(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = r * c  # distance in km
    return d


def get_nearest_park_id(location):
    location_sep = location.split(' ')
    pic_lat = float(location_sep[0])
    pic_lon = float(location_sep[1])
    parks = Park.query.order_by(Park.id).all()
    id_of_closest = None
    distance_of_closest = None  # in km
    for park in parks:
        this_lat = park.get_lat_float()
        this_lon = park.get_lon_float()
        distance = get_distance_in_km(pic_lat, pic_lon, this_lat, this_lon)
        if distance_of_closest == None or distance < distance_of_closest:
            distance_of_closest = distance
            id_of_closest = park.get_id()
    return id_of_closest


def get_pictures_for_tag(tag_name):
    tag_pictures = []
    all_pictures = Picture.query.order_by(Picture.id).all()
    for picture in all_pictures:
        if picture.has_tag(tag_name):
            tag_pictures.append(picture)
    return tag_pictures


def get_tag_cloud_entry_html(tag_name):
    entry_html = ''
    # we'll have ~10 unique tag styles, get random number in there
    rand = random.randrange(1, 11)  # ceiling is not inclusive...
    entry_html += '<a class="btn btn-primary tag-'
    entry_html += str(rand)
    entry_html += '" href="'
    tag_url = app.config.get('BASE_URL') + '/tag/' + tag_name
    entry_html += tag_url
    entry_html += '" role="button">'
    entry_html += tag_name
    entry_html += '</a>'
    return entry_html



def get_tag_cloud_html():
    tag_cloud_html = ''
    # this is horribly inefficient but we're going to aggregate unique tags!
    all_pictures = Picture.query.order_by(Picture.id).all()
    all_tags = []
    for picture in all_pictures:
        tags = picture.get_tags_list()
        for tag in tags:
            if tag not in all_tags:
                all_tags.append(tag)
    # now we have all the unique tags and just need to make a cloud
    for tag in all_tags:
        tag_cloud_html += get_tag_cloud_entry_html(tag)
    return tag_cloud_html


def get_random_pictures(quantity):
    random_pictures = []
    query = db.session.query(Picture)
    row_count = int(query.count())
    for _ in range(quantity):
        rand = random.randrange(1, row_count + 1)
        rand_picture = Picture.query.get(rand)
        if rand_picture is not None:
            random_pictures.append(rand_picture)
    return random_pictures


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


@imagery_blueprint.route('/explore')
def explore():
    tag_cloud_html = get_tag_cloud_html()
    random_pictures = get_random_pictures(12)
    return render_template('imagery/explore.html', tag_cloud=tag_cloud_html, pictures=random_pictures, \
                                                                    is_authenticated=current_user.is_authenticated)


@imagery_blueprint.route('/tag/<tag_name>')
def tag(tag_name):
    pictures = get_pictures_for_tag(tag_name)
    return render_template('imagery/tag.html', tag_name=tag_name, \
                                pictures=pictures, is_authenticated=current_user.is_authenticated)


@imagery_blueprint.route('/image-details/<int:picture_id>')
def image_details(picture_id):
    picture = Picture.query.get(picture_id)
    if picture == None:
        return render_template('errors/404.html'), 404
    return render_template('imagery/details.html', picture=picture, is_authenticated=current_user.is_authenticated)
