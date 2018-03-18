# project/server/main/views.py


from flask import render_template, Blueprint
from flask_login import current_user


main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
def home():
    return render_template('main/home.html', is_authenticated=current_user.is_authenticated)


@main_blueprint.route('/about')
def about():
    return render_template('main/about.html', is_authenticated=current_user.is_authenticated)
