#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import getpass
from StringIO import StringIO
from fabric.api import *
from fabric.contrib.files import exists
from fabric.utils import abort, puts
# from fabric.contrib.project import rsync_project
from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = os.path.dirname(__file__)
env.user = 'deploy'


@task
def staging():
    env.environment = 'staging'
    env.hosts = ['portland.pynorth.org']
    env.site_hostname = 'staging.2017.pycon.ca'
    env.root = '/srv/www/pycon.ca/staging.2017/django'
    env.branch = 'development'

    env.db_name = 'pycon2017_staging'
    env.db_user = 'symposion'
    env.workers = 1
    env.db_pass = getpass.getpass(prompt="Please enter database (%(db_name)s) password for user %(db_user)s: " % env)

    env.allowed_hosts = 'staging.2017.pycon.ca'
    env.django_secret_key = 'yas%wsbwc7mqt#z1i5+s*2ut4#^+_^@%y!#ny)ca4%dpua2ce('

    setup_path()


@task
def production():
    raise Exception('Not yet, cowboy')
    env.environment = 'production'
    env.hosts = ['portland.pynorth.org']
    env.site_hostname = '2017.pycon.ca'
    env.root = '/srv/www/pycon.ca/2017/django'
    env.branch = 'master'

    env.db_name = 'pycon2017'
    env.db_user = 'symposion'
    env.workers = 2
    env.db_pass = getpass.getpass(prompt="Please enter database (%(db_name)s) password for user %(db_user)s: " % env)

    env.allowed_hosts = '2017.pycon.ca,pycon.ca'
    env.django_secret_key = ''  # FIXME

    setup_path()


def setup_path():
    env.slackbot_token = getpass.getpass(prompt="Please enter slackbot token: ")
    env.code_root = os.path.join(env.root, 'pyconca2017')
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.logs_root = os.path.join(env.root, 'logs')
    env.run_root = os.path.join(env.root, 'run')


@task
def deploy():
    require('environment')

    # Create a directory on a remote server, if it doesn't already exists
    if not exists(env.code_root):
        sudo('mkdir -p %(code_root)s' % env)

    if not exists(env.logs_root):
        sudo('mkdir -p %(logs_root)s' % env)

    if not exists(env.run_root):
        sudo('mkdir -p %(run_root)s' % env)

    # Create a virtualenv, if it doesn't already exists
    if not exists(env.virtualenv_root):
        with cd(env.root):
            sudo('mkdir env')
            sudo('virtualenv -p python3 env')

    local('git archive --format=tar %(branch)s | gzip > release.tar.gz' % env)
    put('release.tar.gz', env.code_root, use_sudo=True)

    with cd(env.code_root):
        sudo('tar zxf release.tar.gz', pty=True)
        local('rm release.tar.gz')

        # Activate the environment and install requirements
        # run('source %(remote_env_path)s/bin/activate' % env)
        sudo('source %(virtualenv_root)s/bin/activate && pip install --upgrade -r requirements.txt' % env)

        with shell_env(DJANGO_SETTINGS_MODULE='config.settings.production',
                       DATABASE_URL='postgres://%(db_user)s:%(db_pass)s@localhost:5432/%(db_name)s' % env,
                       DJANGO_SECRET_KEY=env.django_secret_key,
                       DJANGO_ADMIN_URL='admin',
                       PYTHONPATH='.'):
            # Collect all the static files
            sudo('%(virtualenv_root)s/bin/python manage.py collectstatic --noinput' % env)

            # Give deploy access to logs and run directories
            sudo('chown -R deploy:deploy %(logs_root)s' % env)
            sudo('chown -R deploy:deploy %(run_root)s' % env)

            # Migrate and Update the database
            run('%(virtualenv_root)s/bin/python manage.py migrate --noinput' % env)
            run('%(virtualenv_root)s/bin/python manage.py pycon_start' % env)
            run('%(virtualenv_root)s/bin/python manage.py create_review_permissions' % env)

        # gunicorn entry script
        put(get_and_render_template('gunicorn_run.sh', env),
            os.path.join(env.run_root, 'gunicorn_run.sh'), use_sudo=True)
        sudo('chmod u+x %(run_root)s/gunicorn_run.sh' % env)

        # put supervisor conf
        put(get_and_render_template('pycon2017.conf', env),
            '/etc/supervisor/conf.d/pycon2017_%(environment)s.conf' % env,
            use_sudo=True)

        # restart supervisor
        sudo('supervisorctl reread && supervisorctl update')
        sudo('supervisorctl restart pycon2017_%(environment)s' % env)

    # Draw a ship
    puts("               |    |    |               ")
    puts("              )_)  )_)  )_)              ")
    puts("             )___))___))___)\            ")
    puts("            )____)____)_____)\\          ")
    puts("          _____|____|____|____\\\__      ")
    puts(" ---------\                   /--------- ")
    puts("   ^^^^^ ^^^^^^^^^^^^^^^^^^^^^           ")
    puts("     ^^^^      ^^^^     ^^^    ^^        ")
    puts("          ^^^^      ^^^                  ")


def get_and_render_template(filename, context):
    jinja_env = Environment(loader=FileSystemLoader('utility/scripts'))
    tmpl = jinja_env.get_template(filename)
    return StringIO(tmpl.render(context))


