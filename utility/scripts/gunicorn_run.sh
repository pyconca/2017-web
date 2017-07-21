#!/bin/bash

NAME="pycon2017_{{ environment }}"
DJANGODIR={{ code_root }}
SOCKFILE={{ run_root }}/gunicorn.sock
USER=deploy
GROUP=deploy
NUM_WORKERS={{ workers }}
DJANGO_WSGI_MODULE=config.wsgi

# Activate the virtual environment
cd $DJANGODIR
source ../env/bin/activate
export `cat ../run/.env | xargs`

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
