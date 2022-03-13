from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    ''' получить manage.py '''
    return f'~/sites/{host}/venv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    ''' обнулить базу данных '''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'kevin@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    ''' обнулить базу данных '''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'kevin@{host}'):
        session_key: str = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()
