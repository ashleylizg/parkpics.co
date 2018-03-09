#project/server/imagery/views.py

from flask import render_template, Blueprint
from flask_login import current_user


imagery_blueprint = Blueprint('imagery', __name__,)

@imagery_blueprint.route('/upload')
@login_required
def upload():
    return render_template('imagery/upload.html', is_authenticated=current_user.is_authenticated)


@imagery_blueprint.route('/mypics')
@login_required
def my_pictures():
    return render_template('imagery/mypics.html', is_authenticated=current_user.is_authenticated)

app.register_blueprint(imagery_blueprint)