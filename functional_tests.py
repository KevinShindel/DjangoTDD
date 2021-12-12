from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from os.path import dirname, join
import unittest

from main.settings import GECKO_DRIVER


class NewVisitorTest(unittest.TestCase):
    ''' тест нового посетителя'''

    def setUp(self) -> None:
        service = Service(executable_path=GECKO_DRIVER, log_path=join(dirname(GECKO_DRIVER), 'log.txt'))
        options = Options()
        self.browser = webdriver.Firefox(service=service, options=options)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Эдит слышала про крутое онлайн приложение неотложных дел.
        self.browser.get('http://localhost:8000')  # Она решает оценить его домашнюю страницу.
        self.assertIn('To-Do', self.browser.title) # Она видит что заголовок говорит о списке неотложных дел.
        self.fail('Закончить тест!')
        # Ей сразу предлагается ввести элемент списка.
        # Она выбирает в текстовом поле 'Купить павлиньи перья'
        # когда она нажимает Enter, страница обновляется и теперь страница содержит 1: Купить павлиньи перья
        # Текстовое поле по прежнему предлагает ее добавить еще один элемент.
        # Она вводит 'Сделать мушку из павлиньих перьев'
        # Снова страница обновляется, и теперь показывает оба элемента списка.
        # Эдит интересно, запомнил ли сайт ее список. Далее она видит что сайт сгенерировал для неё уникальный URL адресс
        # Она посещает его - список по прежнему там.
        # Удовлетворённая она снова ложится спать

    def tearDown(self) -> None:
        self.browser.close()
        self.browser.quit()


if __name__ == '__main__':
    unittest.main(warnings='ignore')
