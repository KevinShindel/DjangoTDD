from os.path import dirname, join

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from functional_tests.base import FunctionalTest
from main.settings import GECKO_DRIVER, PRODUCTION


class NewVisitorTest(FunctionalTest):
    ''' тест нового посетителя '''

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do list', self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        self.assertIn('Start a new Your ToDo list', header_text)

        # She is invited to enter a to-do item straight away
        input_box = self.get_item_input_box()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        input_box.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        input_box = self.get_item_input_box()
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Satisfied, she goes back to sleep

    def test_multi_user_can_start_a_list_at_diff_urls(self):
        ''' многочисленные пользователи могут начать списки по разным url '''
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys('Купить павлиньи перья')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.close()
        self.browser.quit()

        service = Service(executable_path=GECKO_DRIVER, log_path=join(dirname(GECKO_DRIVER), 'log.txt'))
        options = Options()
        if PRODUCTION:
            options.add_argument('--headless')
        self.browser = webdriver.Firefox(service=service, options=options)
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку', page_text)

        input_box = self.get_item_input_box()
        input_box.send_keys('Купить молоко')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

    # def test_can_start_a_list_and_retrieve_it_later(self):
    #     # Эдит слышала про крутое онлайн приложение неотложных дел.
    #     self.browser.get(self.live_server_url)  # Она решает оценить его домашнюю страницу.
    #     self.assertIn('To-Do', self.browser.title) # Она видит что заголовок говорит о списке неотложных дел.
    #     # Ей сразу предлагается ввести элемент списка.
    #     input_box = self.browser.find_element(by=By.ID, value='id_text')
    #     self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')
    #     # Она выбирает в текстовом поле 'Купить павлиньи перья'
    #     input_box.send_keys('Купить павлиньи перья')
    #     # когда она нажимает Enter, страница обновляется и теперь страница содержит 1: Купить павлиньи перья
    #     input_box.send_keys(Keys.ENTER)
    #     self.wait_for_row_in_list_table('1: Купить павлиньи перья')
    #     # Текстовое поле по прежнему предлагает ее добавить еще один элемент.
    #     # Она вводит 'Сделать мушку из павлиньих перьев'
    #     input_box = self.browser.find_element(by=By.ID, value='id_text')
    #     input_box.send_keys('Сделать мушку из павлиньих перьев')
    #     input_box.send_keys(Keys.ENTER)
    #     # Снова страница обновляется, и теперь показывает оба элемента списка.
    #     self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')
    #     # Эдит интересно, запомнил ли сайт ее список. Далее она видит что сайт сгенерировал для неё уникальный URL адресс
    #     # Она посещает его - список по прежнему там.
    #     # Удовлетворённая она снова ложится спать
