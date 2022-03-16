import datetime
import logging
import os.path
import sys
import time
from os.path import dirname, join

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from .server_tools import reset_database

from main.settings import GECKO_DRIVER, SCREEN_DUMP_LOCATION

logger = logging.getLogger('FunctionalTest')

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

    def add_list_item(self, item_text):
        ''' добавить элемент списка '''
        num_rows = len(self.browser.find_elements(by=By.CSS_SELECTOR, value='#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    def setUp(self):
        if self.against_staging:
            reset_database(self.server_host)
        service = Service(executable_path=GECKO_DRIVER, log_path=join(dirname(GECKO_DRIVER), 'log.txt'))
        options = Options()
        self.browser = webdriver.Firefox(service=service, options=options)

    def tearDown(self) -> None:
        ''' демонтаж '''
        if self._test_has_failed:
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.close()
        self.browser.quit()

    @property
    def _test_has_failed(self):
        ''' тест не сработал '''
        return any(error for (method, error) in self._outcome.errors)

    def dump_html(self):
        ''' выгрузить html '''
        filename = self._get_filename() + '.html'
        logger.error(msg=f'HTML file {filename} saved')
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def take_screenshot(self):
        ''' взять скрин экрана '''
        filename = self._get_filename() + '.png'
        logger.error(msg=f'Screenshot file {filename} saved')
        self.browser.get_screenshot_as_file(filename)

    def _get_filename(self):
        ''' получить имя файла '''
        timestamp = datetime.datetime.now().isoformat().replace(':', '.')[:19]
        return f'{SCREEN_DUMP_LOCATION}/{self.__class__.__name__}.{self._testMethodName}-{self._windowid}-{timestamp}'

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
