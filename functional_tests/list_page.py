from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from functional_tests.base import wait


class ListPage:
    ''' страница списка '''

    def __init__(self, test):
        self.test = test

    def get_list_owner(self):
        ''' получить владельца списка '''
        return self.test.browser.find_element(by=By.ID, value='id_list_owner').text

    def get_table_rows(self):
        ''' получить строки таблицы '''
        return self.test.browser.find_elements(by=By.CSS_SELECTOR, value='#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.assertIn(
            row_text, [row.text for row in rows]
        )

    def get_item_input_box(self):
        ''' получить поле ввода для элемента '''
        return self.test.browser.find_element(by=By.ID, value='id_text')

    def add_list_item(self, item_text):
        ''' добавить элемент списка '''
        new_item_no = len(self.get_table_rows()) + 1
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(item_text, new_item_no)
        return self

    def get_share_box(self):
        ''' получить поле для обмена ссылками '''
        return self.test.browser.find_element(by=By.CSS_SELECTOR, value='input=[name="sharee"]')

    def get_shared_with_list(self):
        ''' получить список от того кто им делится '''
        return self.test.browser.find_elemets(by=By.CSS_SELECTOR, value='.list-sharee')

    def share_list_with(self, email):
        ''' поделится списком с '''
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email, [item.text for item in self.get_shared_with_list()]
        ))
