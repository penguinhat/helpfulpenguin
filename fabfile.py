from fabric.api import local, run, cd, env

env.roledefs = {
    'web': ['151.236.220.208']
}

directory = '/srv/helpfulpenguin/django/'

def test():
    local("./manage.py test")

def pull(branch='master'):
    with cd(directory):
        run("git checkout %s" % branch)
        run("git pull")

def deploy():
    with cd(directory):
        # Activate virtualenv
        python = "../venv/bin/python"

        run("%s manage.py collectstatic --noinput" % python)
        run("%s manage.py migrate" % python)
        run("touch helpfulpenguin/wsgi.py")
