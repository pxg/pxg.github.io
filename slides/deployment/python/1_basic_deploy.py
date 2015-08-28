"""
By default the HEAD of the current branch will be pushed to the remote server:
fab stage deploy

If you don't like all the output:
fab stage deploy --hide=stdout
"""
from fabric.api import env, local
from fabric.operations import put, run


def stage():
    env.hosts = ['54.228.188.132']
    env.user = 'ec2-user'
    env.release_dir = '/var/www/goatse.cx'
    env.key_filename = ['~/.ssh/goatse.pem']
    env.git_repo_dir = '/var/www/git_goatase/'


def deploy():
    """
    Main tasks to update the server from the git master branch
    """
    deploy_code()
    install_requirements()
    migrate_database()
    collectstatic()
    reload_server()


def deploy_code(id):
    """
    Git pull then rsync the site live
    """
    with cd(env.git_repo_dir):
        run('git pull')
        run('rsync -av --delete --exclude .git* ./ %s' % env.release_dir)



def reload_server():
    """
    Reload webserver
    """
    run('service uwsgi restart')
    #sudo('service uwsgi restart')
