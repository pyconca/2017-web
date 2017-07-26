#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from StringIO import StringIO

import yaml
from fabric.api import env, sudo, require, cd, local, put, run, task, shell_env
from fabric.contrib.files import exists
from fabric.utils import puts
from fabric.colors import blue, magenta, white
from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = os.path.dirname(__file__)
env.user = 'deploy'

yell = puts


def load_secrets():
    required = {'db_user', 'db_pass', 'slackbot_token', 'django_secret_key',
                'django_debug'}
    with open('secret.yml') as f:
        secrets = yaml.load(f)

    env_secrets = secrets[env.environment]
    missing_keys = required.difference(set(env_secrets.keys()))
    assert len(missing_keys) == 0, "missing some keys {}".format(missing_keys)
    for key, value in env_secrets.iteritems():
        setattr(env, key, value)


@task
def staging():
    env.environment = 'staging'

    yell(magenta('Configuring {} environment...'.format(env.environment)))
    env.hosts = ['portland.pynorth.org']
    env.site_hostname = 'staging.2017.pycon.ca'
    env.root = '/srv/www/pycon.ca/staging.2017/django'
    env.branch = 'master'
    env.db_name = 'pycon2017_staging'
    env.workers = 1
    env.allowed_hosts = 'staging.2017.pycon.ca'

    yell(magenta('Setting up paths...'))
    setup_path()

    yell(magenta('Learning secrets...'))
    load_secrets()


@task
def production():
    env.environment = 'production'

    yell(magenta('Configuring {} environment...'.format(env.environment)))
    env.hosts = ['portland.pynorth.org']
    env.site_hostname = '2017.pycon.ca'
    env.root = '/srv/www/pycon.ca/2017/django'
    env.branch = 'master'
    env.db_name = 'pycon2017'
    env.workers = 2
    env.allowed_hosts = '2017.pycon.ca,pycon.ca'

    yell(magenta('Setting up paths...'))
    setup_path()

    yell(magenta('Learning secrets...'))
    load_secrets()


def setup_path():
    env.code_root = os.path.join(env.root, 'pyconca2017')
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.logs_root = os.path.join(env.root, 'logs')
    env.run_root = os.path.join(env.root, 'run')


@task
def deploy():
    require('environment')

    yell(magenta("Create a directory on a remote server, if it doesn't already exists"))
    if not exists(env.code_root):
        sudo('mkdir -p %(code_root)s' % env)

    if not exists(env.logs_root):
        sudo('mkdir -p %(logs_root)s' % env)

    if not exists(env.run_root):
        sudo('mkdir -p %(run_root)s' % env)

    yell(magenta("Create a virtualenv, if it doesn't already exists..."))
    if not exists(env.virtualenv_root):
        with cd(env.root):
            sudo('mkdir env')
            sudo('virtualenv -p python3 env')

    local('git archive --format=tar %(branch)s | gzip > release.tar.gz' % env)
    put('release.tar.gz', env.code_root, use_sudo=True)

    with cd(env.code_root):
        sudo('tar zxf release.tar.gz', pty=True)
        local('rm release.tar.gz')

        yell(magenta("Activate the environment and install requirements..."))
        # run('source %(remote_env_path)s/bin/activate' % env)
        sudo('source %(virtualenv_root)s/bin/activate && pip install --upgrade -r requirements.txt' % env)

        django_debug = 1

        if env.environment == 'production':
            django_debug = 0

        with shell_env(DJANGO_SETTINGS_MODULE='config.settings.production',
                       DATABASE_URL='postgres://%(db_user)s:%(db_pass)s@localhost:5432/%(db_name)s' % env,
                       DJANGO_SECRET_KEY=env.django_secret_key,
                       DJANGO_ADMIN_URL='admin',
                       PYTHONPATH='.',
                       DJANGO_DEBUG=django_debug):
            yell(magenta("Collect all the static files..."))
            sudo('%(virtualenv_root)s/bin/python manage.py collectstatic --noinput' % env)

            yell(magenta("Compiling translations..."))
            sudo('%(virtualenv_root)s/bin/python manage.py compilemessages --use-fuzzy' % env)

            yell(magenta("Give deploy access to logs and run directories..."))
            sudo('chown -R deploy:deploy %(logs_root)s' % env)
            sudo('chown -R deploy:deploy %(run_root)s' % env)

            yell(magenta("Migrate and Update the database..."))
            run('%(virtualenv_root)s/bin/python manage.py migrate --noinput' % env)

        yell(magenta("bootstrap environment..."))
        put(get_and_render_template('template.env', env),
            os.path.join(env.run_root, '.env'), use_sudo=True)

        yell(magenta("gunicorn entry script..."))
        put(get_and_render_template('gunicorn_run.sh', env),
            os.path.join(env.run_root, 'gunicorn_run.sh'), use_sudo=True)
        sudo('chmod u+x %(run_root)s/gunicorn_run.sh' % env)

        yell(magenta("put supervisor conf..."))
        put(get_and_render_template('pycon2017.conf', env),
            '/etc/supervisor/conf.d/pycon2017_%(environment)s.conf' % env,
            use_sudo=True)

        yell(magenta("restart supervisor..."))
        sudo('supervisorctl reread && supervisorctl update')
        sudo('supervisorctl restart pycon2017_%(environment)s' % env)

    yell(magenta("Draw a ship..."))
    yell(  white("               |    |    |               "))  # NOQA
    yell(  white("              )_)  )_)  )_)              "))  # NOQA
    yell(  white("             )___))___))___)\            "))  # NOQA
    yell(  white("            )____)____)_____)\\          "))  # NOQA
    yell(magenta("          _____|____|____|____\\\__      "))
    yell(magenta(" ---------\                   /--------- "))
    yell(   blue("   ^^^^^ ^^^^^^^^^^^^^^^^^^^^^           "))  # NOQA
    yell(   blue("     ^^^^      ^^^^     ^^^    ^^        "))  # NOQA
    yell(   blue("          ^^^^      ^^^                  "))  # NOQA


def get_and_render_template(filename, context):
    jinja_env = Environment(loader=FileSystemLoader('utility/scripts'))
    tmpl = jinja_env.get_template(filename)
    return StringIO(tmpl.render(context))
