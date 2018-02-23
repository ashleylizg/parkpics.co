# parkpics.co

Web app that curates national park pictures.

## Quickstart

```
# This is all for Powershell, figure it out otherwise

git clone <this_repo>
cd <this_repo>

# Make sure virtualenv is installed then do this
virtualenv env

# Activate the virtualenv, for Powershell you would do...
.\env\scripts\activate.ps1

# Install the requirements (you only have to do this once)
pip install -r requirements.txt

# Do one of the following
set-variable -name "APP_SETTINGS" -value "project.server.config.DevelopmentConfig"
set-variable -name "APP_SETTINGS" -value "project.server.config.ProductionConfig"

python manage.py create_db
python manage.py db init
python manage.py db migrate
python manage.py create_admin
python manage.py create_data

# Do one of the following
set-variable -name "FLASK_DEBUG" -value True; python manage.py run
set-variable -name "FLASK_DEBUG" -value False; python manage.py run
```

Access the application at [http://localhost:5000](http://localhost:5000).
