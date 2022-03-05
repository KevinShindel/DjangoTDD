from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    '''тест макета и стилевого оформления '''

    def test_layout_and_styling(self):
        ''' тест: стилевого оформления '''

        self.browser.get(self.live_server_url)
        self.browser.set_window_size(width=1024, height=768)

        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)

        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        input_box = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(input_box.location['x'] + input_box.size['width'] / 2, 512, delta=10)


