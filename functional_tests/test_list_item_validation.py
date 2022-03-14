from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    ''' тест валидации элемента списка '''

    def get_error_element(self):
        ''' получить элемент с ошибкой '''
        return self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error')

    def test_cannot_add_empty_list_items(self):
        ''' тест: нельзя добавлять пустые елементы списка '''

        # Эдит открывает страницу и случайно пытается отправить пустой элемент. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='#id_text:invalid'))

        # Эдит начинает набирать текст нового элемента и ошибка изчезает
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='#id_text:valid'))

        # И она может отрпавить его успешно
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # как ни странно Эдит решает отправить второй пустой элемент списка
        self.get_item_input_box().send_keys(Keys.ENTER)

        # и снова браузер не подчинится
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='#id_text:invalid'))

        # И она может исправится, заполнив поле текстом
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        ''' тест нельзя добавить повторяющиеся элементы'''
        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy wellies')
        # self.get_item_input_box().send_keys('Buy wellies')
        # self.get_item_input_box().send_keys(Keys.ENTER)
        # self.wait_for_row_in_list_table('1: Buy wellies')

        # Она случайно пытается ввести повторябщийся элемент
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text, "You've already got this in your list"))

    def test_error_messages_are_cleared_on_input(self):
        ''' тест сообщения об ошибках очищаются при вводе'''
        # Эдит начинает список и вызывает ошибку валидации
        self.browser.get(self.live_server_url)

        self.add_list_item('Banter too think')
        # self.get_item_input_box().send_keys('Banter too think')
        # self.get_item_input_box().send_keys(Keys.ENTER)
        # self.wait_for_row_in_list_table('1: Banter too think')

        self.get_item_input_box().send_keys('Banter too think')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # Она начинает набирать в поле ввода, что бы очистить ошибку
        self.get_item_input_box().send_keys('a')

        # Она довольна от того, что сообщение об ошибке изчезает
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
