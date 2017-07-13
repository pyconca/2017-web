#!/bin/bash

NAME="pycon2017_{{ environment }}"
DJANGODIR={{ code_root }}
SOCKFILE={{ run_root }}/gunicorn.sock
USER=deploy
GROUP=deploy
NUM_WORKERS={{ workers }}
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_WSGI_MODULE=config.wsgi
DATABASE_URL=postgres://{{ db_user }}:{{ db_pass }}@localhost:5432/{{ db_name }}
SLACKBOT_TOKEN={{ slackbot_token }}

# Activate the virtual environment
cd $DJANGODIR
source ../env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export DATABASE_URL=$DATABASE_URL
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
export SLACKBOT_TOKEN='$SLACKBOT_TOKEN'
export DJANGO_ADMIN_URL=admin
export DJANGO_ALLOWED_HOSTS='{{ allowed_hosts }}'
export DJANGO_SECRET_KEY='{{ django_secret_key }}'
export DJANGO_DEBUG=1

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec {{ virtualenv_root }}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
