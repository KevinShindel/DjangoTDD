from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

from functional_tests.base import FunctionalTest
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model

User = get_user_model()


class MyListTest(FunctionalTest):
    ''' тест приложения мои списки '''

    def create_pre_auth_session(self, email):
        ''' создать предварительно аутентифицированный сеанс '''
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # установить cookie, которые нужны для первого посещения домена
        # страницы 404 загружаются быстрее всего
        self.browser.get(self.live_server_url + "/404_no_such_url")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session.session_key,
                path='/'
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        ''' тест списки зарегистрированых пользователей сохраняются как мои списки '''
        email = 'test@mail.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email=email)

        # Эдит является зарегистрированым пользователем
        self.create_pre_auth_session(email=email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email=email)
