import time
from os.path import dirname, join

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from main.settings import GECKO_DRIVER, STAGING_SERVER, PRODUCTION


class FunctionalTest(StaticLiveServerTestCase):
    MAX_WAIT = 3

    def setUp(self) -> None:
        service = Service(executable_path=GECKO_DRIVER, log_path=join(dirname(GECKO_DRIVER), 'log.txt'))
        options = Options()
        if PRODUCTION:
            options.add_argument('--headless')
        self.browser = webdriver.Firefox(service=service, options=options)
        staging_server = STAGING_SERVER
        if staging_server is not None:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self) -> None:
        self.browser.close()
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str) -> None:
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
