from django.contrib.auth import get_user_model

from functional_tests.base import FunctionalTest

User = get_user_model()


class MyListTest(FunctionalTest):
    ''' тест приложения мои списки '''

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        ''' тест списки зарегистрированых пользователей сохраняются как мои списки '''
        email = 'test@mail.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email=email)

        # Эдит является зарегистрированым пользователем
        # Она заходит на главную страницу и создает новй список
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # Она увидела ссылку 'My lists' впервые
        self.browser.find_element_by_link_text('My lists').click()

        # замечает что список назван по первому элементу
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Она решает создать другой список
        self.browser.get(self.server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Она видит что появилась ссылка на новый список
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows')
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Она разлогинилась. Ссылка "My lists" паропала.
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))
