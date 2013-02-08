from fabric.api import local, run, cd, env

env.roledefs = {
    'web': ['151.236.220.208']
}

directory = '/srv/helpfulpenguin/django/'

def qtest():
    local("./manage.py test frontend redirects --failfast")

def pull(branch=None):
    with cd(directory):
        if branch:
            run("git checkout %s" % branch)
        run("git pull")

def deploy():
    with cd(directory):
        # Activate virtualenv
        python = "../venv/bin/python"

        run("%s manage.py collectstatic --noinput" % python)
        run("%s manage.py migrate" % python)
        run("touch helpfulpenguin/wsgi.py")


def service_start(service):
    run("sudo service %s start" % service)

def service_stop(service):
    run("sudo service %s stop" % service)

def service_restart(service):
    run("sudo service %s restart" % service)
