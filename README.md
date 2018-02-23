# parkpics.co

Web app that curates national park pictures.

## Quickstart

```
cd parkpics.co

# Make sure virtualenv is installed then do this
virtualenv env

# Activate the virtualenv, for Powershell you would do...
.\env\scripts\activate.ps1

# Install the requirements (you only have to do this once)
pip install -r requirements.txt

# Do one of the following
export APP_SETTINGS="project.server.config.DevelopmentConfig"
export APP_SETTINGS="project.server.config.ProductionConfig"

python manage.py create_db
python manage.py db init
python manage.py db migrate
python manage.py create_admin
python manage.py create_data

# Do one of the following
export FLASK_DEBUG=1 && python manage.py run
export FLASK_DEBUG=0 && python manage.py run
```

Access the application at [http://localhost:5000](http://localhost:5000).
