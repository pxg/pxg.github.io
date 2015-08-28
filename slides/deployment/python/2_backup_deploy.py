"""
By default the HEAD of the current branch will be pushed to the remote server:
fab stage deploy

This can be overridden by providing a hash:
fab stage deploy:2ab1c583e35c99b66079877d49e3ec03812d3e53

If you don't like all the output:
fab stage deploy --hide=stdout
"""
import os

from fabric.api import env, local
from fabric.operations import put, run
from fabric.context_managers import cd


def stage():
    env.hosts = ['54.228.188.132']
    env.user = 'ec2-user'
    # Note: the site root is now /var/www/goatse.cx/current
    # Previous releases can be found in /var/www/goatse.cx/releases/<hash>
    env.release_dir = '/var/www/goatse.cx'
    env.key_filename = ['~/.ssh/goatse.pem/']


def deploy(id='HEAD'):
    """
    Main tasks to update the server from the given commit id, will use the
    HEAD of the current branch by default
    """
    release_dir = deploy_code(id)
    install_requirements(release_dir)
    backup_database()
    migrate_database(release_dir)
    collectstatic(release_dir)
    switch_release(release_dir)
    reload_server()


def deploy_code(id):
    """
    Package the code for the commit id, move it to the server, then clean-up
    """
    # Package code
    hash = local('git rev-parse %s' % id, capture=True)
    file = '%s.tar.gz' % hash
    local('git archive --format tar.gz %s -o %s' % (id, file))

    # Put code on server
    release_dir = os.path.join(env.release_dir, 'releases', hash)
    run('mkdir -p %s' % release_dir)
    put(file, release_dir)
    with cd(release_dir):
        run('tar -xf %s' % file)

    # Clean-up
    local('rm %s' % file)


def switch_release(release_dir):
    """
    Switch symlink so the newly deployed code is live
    """
    with cd(env.release_dir):
        run('ln -sfn %s current' % release_dir)
