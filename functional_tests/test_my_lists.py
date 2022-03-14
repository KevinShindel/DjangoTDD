from django.conf import settings
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_pre_authenticated_session
from .server_tools import create_session_on_server

User = get_user_model()


class MyListTest(FunctionalTest):
    ''' тест приложения мои списки '''

    def create_pre_auth_session(self, email):
        ''' создать предварительно аутентифицированный сеанс '''

        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)

        # установить cookie, которые нужны для первого посещения домена
        # страницы 404 загружаются быстрее всего
        self.browser.get(self.live_server_url + "/404_no_such_url")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
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
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # Она замечает ссылку на Мои списки в первый раз
        self.browser.find_element(by=By.LINK_TEXT, value='My lists').click()
        # Она видит что ее список находится там и он назван на основе первого элемента
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT, value='Reticulate splines')
        )
        self.browser.find_element(by=By.LINK_TEXT, value='Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Она решает начать еще один список что бы только убедится
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Под заголовком Мои Списки поялвяется ее новый список
        self.browser.find_element(by=By.LINK_TEXT, value='CLick cows')
        self.browser.find_element(by=By.LINK_TEXT, value='CLick cows').click()
        self.wait_for(
            self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Она выходит из системы. Опция мои списки изчезает
        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(by=By.LINK_TEXT, value='My lists'),
                []
            )
        )
