# project/server/user/views.py


import os
import uuid

from flask import current_app as app
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required

from project.server import bcrypt, db
from project.server.models import Picture, User
from project.server.user.forms import LoginForm, RegisterForm

from werkzeug.utils import secure_filename


ALLOWED_UPLOAD_EXTENSIONS = set(['jpg','jpeg','png','gif'])


user_blueprint = Blueprint('user', __name__,)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash('Thank you for registering.', 'success')
        return redirect(url_for('user.members'))

    return render_template('user/register.html', form=form, is_authenticated=current_user.is_authenticated)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('user.members'))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form, is_authenticated=current_user.is_authenticated)
    return render_template('user/login.html', title='Please Login', form=form, is_authenticated=current_user.is_authenticated)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('main.home'))


@user_blueprint.route('/members')
@login_required
def members():
    return render_template('user/members.html', is_authenticated=current_user.is_authenticated)


def is_allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS


@user_blueprint.route('/upload', methods=['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filesize = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            picture = Picture(
                owner_id=str(current_user),
                filename=filename,
                filesize=filesize,  # in the future we may scale down files, thus the 2 fields
                original_filename=original_filename,
                original_filesize=filesize
            )
            db.session.add(picture)
            db.session.commit()
            flash('Upload successful.', 'success')
            return redirect(url_for('user.my_pictures'))
    # here it's a GET and we render the template
    return render_template('user/upload.html', is_authenticated=current_user.is_authenticated)


@user_blueprint.route('/img/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@user_blueprint.route('/mypics')
@login_required
def my_pictures():
    return render_template('user/mypics.html', is_authenticated=current_user.is_authenticated)
