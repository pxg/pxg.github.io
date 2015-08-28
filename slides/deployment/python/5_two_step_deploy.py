"""
By default the HEAD of the current branch will be pushed to the remote server:
fab stage deploy

This can be overridden by providing a hash:
fab stage deploy:2ab1c583e35c99b66079877d49e3ec03812d3e53

If you don't like all the output:
fab stage deploy --hide=stdout
"""
import os

from fabric.api import env, execute, local, parallel
from fabric.operations import run, put
from fabric.context_managers import cd, prefix
from fabric.decorators import roles


def stage():
    env.roledefs = {
        'web': ['ubuntu@54.228.188.132', 'ubuntu@54.228.188.133'],
        'master': ['ubuntu@54.228.188.132']
    }
    env.user = 'ec2-user'
    # Note: the site root is now /var/www/goatse.cx/current
    # Previous releases can be found in /var/www/goatse.cx/releases/<hash>
    env.release_dir = '/var/www/goatse.cx'
    env.key_filename = ['~/.ssh/goatse.pem/']
    env.git_repo_dir = '/var/www/git_goatase/'
    env.venv_activate = '/var/lib/venv/goatse/bin/activate'


def deploy(id='HEAD'):
    """
    Main tasks to update the server from the given commit id, will use the
    HEAD of the current branch by default
    """
    release_dir = prepare_deploy(id)
    activate_deploy(release_dir)


def prepare_deploy(id='HEAD'):
    """
    Execute all steps which can in advance of actually switching the site live
    This is done to speed up activating deployments
    """
    packaged_code, release_dir = _package_code(id)
    execute(deploy_package, packaged_code, release_dir)
    execute(install_requirements, release_dir)
    execute(backup_database)
    execute(collectstatic, release_dir)
    _clean_up(packaged_code)
    return release_dir


def activate_deploy(release_dir):
    """
    Switch the deployment to being live. This is the risk zone where downtime
    could potentially happen.
    """
    execute(migrate_database, release_dir)
    execute(switch_release, release_dir)
    execute(reload_server)


def _package_code(id):
    """
    Locally compress the git repo into an archive, and generate the release dir
    variable
    """
    hash = local('git rev-parse %s' % id, capture=True)
    file = '%s.tar.gz' % hash
    local('git archive --format tar.gz %s -o %s' % (id, file))

    release_dir = os.path.join(env.release_dir, 'releases', hash)
    return file, release_dir


@parallel
@roles('web')
def deploy_package(file, release_dir):
    """
    Move the packaged code to the webservers
    """
    run('mkdir -p %s' % release_dir)
    put(file, release_dir)

    with cd(release_dir):
        run('tar -xf %s' % file)


def _clean_up(packaged_code):
    """
    Delete the packaged code
    """
    local('rm %s' % packaged_code)
