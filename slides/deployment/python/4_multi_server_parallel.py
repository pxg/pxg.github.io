from fabric.api import parallel
from fabric.decorators import roles


def stage():
    env.roledefs = {
        'web': ['ubuntu@54.228.188.132', 'ubuntu@54.228.188.133'],
        'master': ['ubuntu@54.228.188.132']
    }
    env.venv_activate = '/var/lib/venv/goatse/bin/activate'


def deploy(id='HEAD'):
    """
    Main tasks to update the server from the given commit id, will use the
    HEAD of the current branch by default
    """
    release_dir = execute(deploy_code, id)
    execute(install_requirements, srelease_dir)
    execute(backup_database)
    execute(migrate_database, release_dir)
    execute(collectstatic, release_dir)
    execute(switch_release, release_dir)
    execute(reload_server)


@parallel
@roles('web')
def switch_release(release_dir):
    """
    Switch symlink so the newly deployed code is live
    """
    with cd(env.release_dir):
        run('ln -sfn %s current' % release_dir)


@parallel
@roles('web')
def reload_server():
    """
    Reload webserver
    """
    run('service uwsgi restart')


@roles('master')
def migrate_database(release_dir):
    with cd(release_dir):
        with prefix('source ' + env.venv_activate):
            run('python manage.py syncdb --migrate --noinput')
