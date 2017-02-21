Development Environment Setup
=============================

You will need the following:

* Python >= 3.5
* pip
* virtualenvwrapper
* Postgres >= 9.5

Start by cloning the repository

    $ git clone git@github.com:pyconca/2017-web.git
    $ cd 2017-web

Create a Python virtual environment:

    ~/2017-web $ mkvirtualenv pycon.ca-2017
    (pycon.ca-2017) ~/2017-web $

The (pycon.ca-2017) prefix indicates that a virtual environment called "pycon.ca-2017" is being used. Next, check that you have the correct version of Python:

    (pycon.ca-2017) ~/2017-web $ python --version
    Python 3.6.0
    (pycon.ca-2017) ~/2017-web $ pip --version
    pip 9.0.1 from /Users/.../site-packages (python 3.6)

Install the project requirements:

    (pycon.ca-2017) ~/2017-web $ pip install -U -r requirements/local.txt

Create the Postgres database:

    (pycon.ca-2017) ~/2017-web $ createdb pyconca2017

You can now run the usual Django `migrate` command to setup the database:

    (pycon.ca-2017) ~/2017-web $ python manage.py migrate

Next create a super user:

    (pycon.ca-2017) ~/2017-web $ python manage.py createsuperuser

Now run the develop web server:

(pycon.ca-2017) ~/2017-web $ python manage.py runserver
