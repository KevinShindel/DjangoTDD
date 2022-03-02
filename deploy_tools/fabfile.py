import random

from fabric.api import env, local, run
from fabric.contrib.files import append, exists, sed
from string import ascii_lowercase, digits

REPO_URL = 'https://github.com/KevinShindel/DjangoTDD'


def deploy():
    site_folder = f'/opt/DjangoTDD'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtual_env(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    ''' создать папки '''
    for sub_folder in ('static', 'venv', 'source'):
        run(f'mkdir -p {site_folder}/{sub_folder}')


def _get_latest_source(source_folder):
    ''' обновить код с репозитория '''
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
        current_commit = local(command='git log -n 1 --format=%H', capture=True)
        run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    ''' обновить настройки '''
    settings_path = source_folder + '/main/settings.py'
    sed(settings_path, 'DEBUG=True', 'DEBUG=False')
    sed(settings_path, 'ALLOWED_HOSTS = .+$', f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key = source_folder + '/main/secret_key.py'
    if not exists(secret_key):
        chars = ascii_lowercase + digits
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtual_env(source_folder):
    ''' обновить зависимости '''
    virtualenv_folder = source_folder + '/../venv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.8 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    ''' обновить статические файлы '''
    run(f'cd {source_folder} &&  ../venv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    ''' обновить базу данных '''
    run(f'cd {source_folder} && ../venv/bin/python manage.py migrate --noinput')


if __name__ == '__main__':
    deploy()
