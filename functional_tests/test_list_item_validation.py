from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    ''' тест валидации элемента списка '''

    def test_cannot_add_empty_list_items(self):
        ''' тест: нельзя добавлять пустые елементы списка '''

        # Эдит открывает страницу и случайно пытается отправить пустой элемент. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.ID, value='id_text').send_keys(Keys.ENTER)

        # домашняя страница обновляется, и появляется сообщение об ошибке которое говорит, что елементы списка не должны
        # быть пустыми
        fn = lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error')
        self.wait_for(fn=fn)

        # Она пробует снова, теперь с неким текстом для елемента, и теперь это срабатывает
        #         Как ни странно, Эдит решает отправить второй пустой елемент списка

        input_box = self.browser.find_element(by=By.ID, value='id_text')
        actions = ActionChains(driver=self.browser).click(input_box).send_keys('Buy milk').send_keys(Keys.ENTER)
        actions.perform()
        self.wait_for_row_in_list_table('1: Buy milk')

        # Она получает аналогичное предупреждение на странице списка
        self.browser.find_element(by=By.ID, value='id_text').send_keys(Keys.ENTER)
        fn = lambda: self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error')
        self.wait_for(fn)

        # и она может его исправить , заполнив поле неким текстом
        input_box = self.browser.find_element(by=By.ID, value='id_text')
        actions = ActionChains(driver=self.browser).click(input_box).send_keys('Make tea').send_keys(Keys.ENTER)
        actions.perform()

        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
