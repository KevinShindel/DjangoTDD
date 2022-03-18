from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest
from functional_tests.list_page import ListPage
from functional_tests.my_list_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.close()
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    ''' тест обмена данными '''

    def test_can_share_a_list_with_another_user(self):
        ''' тест можно обмениватся списком с еще одним пользователем '''
        # Эдит является зарегистрированным пользователем
        self.create_pre_authenticated_session('some@example.com')
        edith_browser = self.browser
        self.addCleanup(
            lambda: quit_if_possible(edith_browser)
        )

        # её друг Анцифер тоже зависает на сайте списков
        oni_browser = self.create_browser()
        self.addCleanup(
            lambda: quit_if_possible(oni_browser)
        )
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferus@mail.com')

        # Эдит открывает домащнюю страницу и начинает новый список
        self.browser = edith_browser
        list_page = ListPage(self).add_list_item('Get help')

        # Она замечает опцию "Поделится этим списком"
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        list_page.share_list_with('oniciferus@mail.com')
        # Анцифер переходит на страницу списков в своем браузере
        self.browser = oni_browser
        MyListsPage(self).got_to_my_lists_page()

        # Она видит в ней список Эдит
        self.browser.find_element(by=By.LINK_TEXT, value='Get help').click()

        self.wait_for(lambda:
                      self.assertEqual(
                          list_page.get_list_owner(),
                          'some@example.com')
        )
        # Он добавляент элемент в список
        list_page.add_list_item('Hi Edith!')
        # Когда Эдит обновляет страницу она видит дполнение Анцифера
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith', 2)