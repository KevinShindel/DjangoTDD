import time
from os.path import dirname, join

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from .server_tools import reset_database

from main.settings import GECKO_DRIVER, STAGING_SERVER, PRODUCTION

MAX_WAIT = 3


def wait(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return wrapper


class FunctionalTest(StaticLiveServerTestCase):
    MAX_WAIT = 3

    def setUp(self) -> None:
        service = Service(executable_path=GECKO_DRIVER, log_path=join(dirname(GECKO_DRIVER), 'log.txt'))
        options = Options()
        if PRODUCTION:
            options.add_argument('--headless')
        self.browser = webdriver.Firefox(service=service, options=options)
        self.staging_server = STAGING_SERVER
        if self.staging_server is not None:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self) -> None:
        self.browser.close()
        self.browser.quit()

    def get_item_input_box(self):
        ''' получить поле ввода для элемента '''
        return self.browser.find_element(by=By.ID, value='id_text')

    @wait
    def wait_for_row_in_list_table(self, row_text: str) -> None:
        table = self.browser.find_element(by=By.ID, value='id_list_table')
        rows = table.find_elements(by=By.TAG_NAME, value='tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn) -> None:
        return fn()

    @wait
    def wait_to_be_logged_in(self, email):
        ''' ожидать входа в систему '''
        self.browser.find_element(by=By.LINK_TEXT, value='Log out')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        ''' ожидать выхода из системы '''
        self.browser.find_element(by=By.NAME, value='email')
        navbar = self.browser.find_element(by=By.CSS_SELECTOR, value='.navbar')
        self.assertNotIn(email, navbar.text)
