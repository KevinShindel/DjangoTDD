import time
from os.path import dirname, join

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from main.settings import GECKO_DRIVER


class NewVisitorTest(LiveServerTestCase):

    MAX_WAIT = 3

    def setUp(self) -> None:
        service = Service(executable_path=GECKO_DRIVER, log_path=join(dirname(GECKO_DRIVER), 'log.txt'))
        options = Options()
        self.browser = webdriver.Firefox(service=service, options=options)

    def wait_for_row_in_lista_table(self, row_text: str) -> None:
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value='id_list_table')
                rows = table.find_elements(by=By.TAG_NAME, value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return None
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Эдит слышала про крутое онлайн приложение неотложных дел.
        self.browser.get(self.live_server_url)  # Она решает оценить его домашнюю страницу.
        self.assertIn('To-Do', self.browser.title) # Она видит что заголовок говорит о списке неотложных дел.
        # Ей сразу предлагается ввести элемент списка.
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')
        # Она выбирает в текстовом поле 'Купить павлиньи перья'
        input_box.send_keys('Купить павлиньи перья')
        # когда она нажимает Enter, страница обновляется и теперь страница содержит 1: Купить павлиньи перья
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_lista_table('1: Купить павлиньи перья')
        # Текстовое поле по прежнему предлагает ее добавить еще один элемент.
        # Она вводит 'Сделать мушку из павлиньих перьев'
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        input_box.send_keys(Keys.ENTER)
        # Снова страница обновляется, и теперь показывает оба элемента списка.
        self.wait_for_row_in_lista_table('2: Сделать мушку из павлиньих перьев')
        # Эдит интересно, запомнил ли сайт ее список. Далее она видит что сайт сгенерировал для неё уникальный URL адресс
        # Она посещает его - список по прежнему там.
        # Удовлетворённая она снова ложится спать

    def tearDown(self) -> None:
        self.browser.close()
        self.browser.quit()
