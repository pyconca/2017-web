from os.path import join

from fabric.api import env, task, local
from fabric.utils import abort, puts
from fabric.contrib.project import rsync_project

env.user = 'deploy'
env.hosts = ['portland.pynorth.org']
env.use_ssh_config = True

env.root_dir = '/srv/www/pycon.ca/2017/'
env.html_dir = join(env.root_dir, 'html')


@task
def deploy():
    git_status = local('git status --porcelain', capture=True)

    if git_status:
        abort('There are unchecked files.')

    rsync_project(remote_dir=env.html_dir, local_dir='./src/', delete=False,
                  exclude=['.DS_Store'])

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

