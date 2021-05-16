# lemon-api
Django REST Framework project within a Backend Django Framework course

## Getting Started
For correct work you need to create virtual environment with python 3.8.

Creation of virtual environments on Windows is done by executing the command ```venv```:
```
python -m venv /path/to/new/virtual/environment
```
To activate virtualenv on Windows, and activate the script is in the Scripts folder :
```
\pathto\env\Scripts\activate
```
Install needed applications
```
pip install -r requirements.txt
```
Make and apply migrations
```
python manage.py makemigrations
python manage.py migrate
```
Then run server
```
python manage.py runserver
```
