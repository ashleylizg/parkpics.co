# parkpics.co

parkpics is a web app that curates geotagged images of North American state and national parks.

A "my first web app" project meant to introduce Git-based agile and Python web development to [@ashleylizg](https://github.com/ashleylizg) with supervision from [@gingeleski](https://github.com/gingeleski)

## Running locally

For your first run, follow the code below. This was developed with Powershell so mileage may vary with other prompts.

You'll access the application at Flask's default of [http://localhost:5000](http://localhost:5000)

```powershell
git clone <this_repo>
cd parkpics.co

# (optional) This sets up a virtual environment at /env
python -m venv env
# Then this should activate it in Powershell or a Unix terminal...
./env/scripts/activate
# When you see (env) before your prompt you're good to go

# Install the requirements
pip install -r requirements.txt

# We'll use the development configuration
set-variable -name "APP_SETTINGS" -value "project.server.config.DevelopmentConfig"

# Initial database setup
python manage.py create_db
python manage.py db init
python manage.py db migrate

# Makes an administrator with email "ad@min.com" and password "admin"
python manage.py create_admin

# This populates the table "parks" with data from /data/*.csv
python manage.py create_data

set-variable -name "FLASK_DEBUG" -value True
python manage.py run

# The application should be up at http://localhost:5000

# When you're ready to shut down, Ctrl+C should kill the server

# Then exit the virtual environment
deactivate
```

For future runs, the steps abridge down to...

```powershell
cd parkpics.co
./env/scripts/activate
python manage.py run
# Use the application, then Ctrl+C to kill
deactivate
```

## Stack

Frontend = Bootstrap, jQuery

Backend = Flask, sqlite via SQL Alchemy, Clarifai's image recognition API

## Deployment

This hasn't been deployed into production but the license gives you every right to do so.

At the time of this writing parkpics.co is still an available domain name!

Feel free to fork the repo and add deployment scripts too.

---

Made with :heart: for 🌳🌲

Check out [ashleygingeleski.com](http://ashleygingeleski.com) :shipit:
