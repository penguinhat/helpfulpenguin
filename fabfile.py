from fabric.api import local, run, cd, env

env.roledefs = {
    'web': ['151.236.220.208']
}

def test():
    local("./manage.py test")

def deploy():
    directory = '/srv/helpfulpenguin/django/'
    with cd(directory):
        # Activate virtualenv
        python = "../venv/bin/python"

        run("git pull")
        run("%s manage.py collectstatic --noinput" % python)
        run("%s manage.py migrate" % python)
        run("touch helpfulpenguin/wsgi.py")
