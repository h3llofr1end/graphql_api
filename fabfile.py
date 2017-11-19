import os

from fabric.state import env
from fabric.api import cd, run, sudo, settings
from fabric.contrib.files import exists, upload_template


def bootstrap(env_name):
    set_env(env_name)

    install_system_libs()
    create_folders()
    get_src()
    create_virtualenv()
    install_venv_libs()
    configure_nginx()
    configure_uwsgi()
    run_django_postbootstrap_commands()
    restart_all()


def deploy(env_name):
    set_env(env_name)

    update_src()
    install_venv_libs()
    configure_nginx()
    configure_uwsgi()
    run_django_postbootstrap_commands()
    restart_all()


def set_env(env_name):
    if env.name == 'dev':
        env.hosts = ['ssh_user@host']
    else:
        env.hosts = ['ssh_user2@host2']

    env.BASE_SRC_PATH = '/var/www/'
    env.PROJECT_NAME = 'shop'
    env.REMOTE_PROJECT_PATH = os.path.join(env.BASE_SRC_PATH, env.PROJECT_NAME)
    env.GIT_REPO_PATH = 'git://github.com/...'
    env.REMOTE_VENV_PATH = os.path.join(
        env.BASE_SRC_PATH,
        '.virtualenvs',
        env.PROJECT_NAME
    )
    env.BASE_REMOTE_PYTHON_PATH = '/usr/bin/python3.5'
    env.VENV_REMOTE_PYTHON_PATH = os.path.join(
        env.REMOTE_VENV_PATH,
        'bin',
        'python'
    )
    env.DJANGO_CONFIGURATION = 'Prod'


def install_system_libs():
    sudo('apt-get install python3.5-dev nginx')


def create_folders():
    _mkdir(env.REMOTE_PROJECT_PATH)
    _mkdir(env.REMOTE_VENV_PATH)


def get_src():
    if not exists(os.path.join(env.REMOTE_PROJECT_PATH, '.git')):
        run('git clone %s %s' % (env.REMOTE_PROJECT_PATH, env.GIT_REPO_PATH))


def update_src():
    pass


def create_virtualenv():
    if not exists(os.path.join(env.REMOTE_VENV_PATH, 'pyvenv.cfg')):
        run('%s -m venv %s' % (env.BASE_REMOTE_PYTHON_PATH, env.REMOTE_VENV_PATH))


def install_venv_libs():
    run('%s -m pip install -r %s' % (
        env.VENV_REMOTE_PYTHON_PATH,
        os.path.join(env.REMOTE_PROJECT_PATH, 'requirements.txt')
    ))


def configure_nginx():
    _put_template(
        'nginx.conf',
        os.path.join('/etc/nginx/sites-available', env.PROJECT_NAME)
    )
    sites_enabled_link = os.path.join(
        '/etc/nginx/sites-available',
        env.PROJECT_NAME
    )
    if not exists(sites_enabled_link):
        run('ln -ls %s %s' % (
            os.path.join('/etc/nginx/sites-available', env.PROJECT_NAME),
            sites_enabled_link
        ))


def configure_uwsgi():
    pass


def run_django_postbootstrap_commands():
    _run_django_management_command('migrate')
    _run_django_management_command('collectstatic --noinput')


def restart_all():
    run('service nginx restart')
    run('service uwsgi restart')


def _mkdir(path):
    run('mkdir -p %s' % path)


def _put_template(template_name, remote_path, use_sudo=False):
    upload_template(
        os.path.join('deploy_templates', template_name),
        remote_path,
        context={
            'app_name': env.PROJECT_NAME,
        },
        use_sudo=use_sudo,
    )


def _run_django_management_command(command):
    run('DJANGO_CONFIGURATION=%s %s %s %s' % (
        env.DJANGO_CONFIGURATION,
        env.VENV_REMOTE_PYTHON_PATH,
        os.path.join(env.REMOTE_PROJECT_PATH, 'manage.py'),
        command
    ))
