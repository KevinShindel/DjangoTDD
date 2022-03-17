from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


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
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')
        # Она замечает опцию "Поделится этим списком"
        share_box = self.browser.find_element(by=By.CSS_SELECTOR, value='input=[name="sharee"]')
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
