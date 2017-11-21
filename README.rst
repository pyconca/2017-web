PyCon Canada 2017
=================

The website for `PyCon Canada 2017`_.

.. _`PyCon Canada 2017`: https://2017.pycon.ca/

.. image:: https://travis-ci.org/pyconca/2017-web.svg?branch=master
    :target: https://travis-ci.org/pyconca/2017-web

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django



:License: MIT


Setup
-----------

1. Ensure you have `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_ installed. Then use it to create a virtual env to contain all our Python dependencies, and activate it.

   **Note:** Your Python 3 path might be different from the example below. If you're not sure, try running ``which python3``, and using that path instead.

    $ mkvirtualenv 2017-web --python=/usr/bin/python3

    $ workon 2017-web

2. Install our dependencies:

    $ pip install --upgrade -r requirements/local.txt

3. Configure database stuff. Prod uses PosgreSQL. (TODO: outline this step).

   If you just want to get going quickly, replace the DATABASES part of ``config/settings/common.py`` with this snippet:

   .. code-block:: python

     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
             'NAME': 'mydatabase',
         }
     }

4. Set this environment variable for Django, to point it to the settings file it should use:

    $ export DJANGO_SETTINGS_MODULE=config.settings.local

5. Setup and run Django!

    $ python manage.py migrate

    $ python manage.py runserver


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `2017-patterns`_.

.. _`2017-patterns`: https://github.com/pyconca/2017-patterns

Styles development hack

To use statics from the `2017-patterns` repo while developing, use this hack:

    STATICFILES_DIRS = (
        # str(APPS_DIR.path('static')),  # <== default
        str(APPS_DIR.path('../../2017-patterns/dist/assets')),  # use dist from the 2017-patterns repo
    )

When complete, copy the `dist/assets` directory into `pyconca2017/static` directory.


Translations
^^^^^^^^^^^^

When adding new text, use Django's `i18n` module. Translation file is located here: `pyconca2017/locale/fr/LC_MESSAGES/django.po`.

To add new translations, run:

    $ python manage.py makemessages -a

and then add translations to the locale file.

**Full page articles** can be added as `markdown` files `pyconca2017/templates/markdown` under "en" and "fr" directories, and
can be used in template as follows:

    {% include_md 'my_markdown_file.md` %}

Language will be looked up automatically. If translation does not exist, the version will fall back to "en"



Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use `MailHog`_ when generating the project a local SMTP server with a web interface will be available.

.. _mailhog: https://github.com/mailhog/MailHog

To start the service, make sure you have nodejs installed, and then type the following::

    $ npm install
    $ grunt serve

(After the first run you only need to type ``grunt serve``) This will start an email server that listens on ``127.0.0.1:1025`` in addition to starting your Django project and a watch task for live reload.

To view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

The email server will exit when you exit the Grunt task on the CLI with Ctrl+C.




Deployment
----------

To deploy you'd run the `fab` command. Keep in mind, Fabric is only supported for Python 2.

In your Python 2 environment, run:

    $ pip install --upgrade -r requirements/deploy.txt

Before you run the deploy command, make sure you have `secret.yml` (with proper secrets) in the root of the repo.

    fab staging deploy -i <path/to/identity_key>
