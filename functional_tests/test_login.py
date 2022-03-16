import logging
import poplib
import re
import time
from encodings.utf_8 import decode

from django.core import mail
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from accounts.views import SUCCESS_SEND_MAIL
from functional_tests.base import FunctionalTest
from main.settings import YAHOO_HOST, YAHOO_PASSWORD, YAHOO_HOST_PORT

TEST_EMAIL = 'some@mail.com'
SUBJECT = 'Your login link for ToDo lists'

logger = logging.getLogger('LoggingTest')


class LoginTest(FunctionalTest):
    ''' тест регистрации в системе'''

    def wait_for_email(self, test_email, subject):
        ''' ожидать электронное сообщение '''
        if not self.against_staging:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        else:
            email_id = None
            start = time.time()
            inbox = poplib.POP3_SSL(YAHOO_HOST)
            try:
                inbox.user(test_email)
                inbox.pass_(YAHOO_PASSWORD)
                inbox.port = YAHOO_HOST_PORT
                while time.time() - start < 60:
                    ''' получить 10 самых новых сообщений '''
                    count, _ = inbox.stat()
                    for i in reversed(range(max(1, count - 10), count + 1)):
                        logger.info(msg=f'gettin msg {i}')
                        _, lines, __ = inbox.retr(i)
                        lines = [line.decode('utf8') for line in lines]
                        logger.info(msg=lines)
                        if f'Subject: {subject}' in lines:
                            email_id = i
                            body = '\n'.join(lines)
                            return body
                    time.sleep(5)
            finally:
                if email_id:
                    inbox.dele(email_id)
                inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        ''' тест можно получить ссылку по почте для регистрации '''
        # Эжтт заходит на сайт и впервые видит раздел войти в навигационной панели
        # Он говорит ей ввести свой адрес электронной почты что она и делает
        if self.staging_server:
            test_mail = 'kevin.shindel@yahoo.com'
        else:
            test_mail = TEST_EMAIL

        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.NAME, value='email').send_keys(test_mail)
        self.browser.find_element(by=By.NAME, value='email').send_keys(Keys.ENTER)
        # Появляется сообщение которое говорит что на почту было выслано письмо
        self.wait_for(lambda: self.assertIn(
            SUCCESS_SEND_MAIL, self.browser.find_element(by=By.TAG_NAME, value='body').text
        ))
        # Эдит проверяет свою почту и находит сообщение
        body = self.wait_for_email(test_email=test_mail, subject=SUBJECT)

        # Оно содержит ссылку на url-адресс
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n {body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Эдит нажимает на cсылку
        self.browser.get(url)

        # Она зарегистрирована в системе
        self.wait_to_be_logged_in(email=test_mail)

        # Теперь она выходит из системы
        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()

        # Она вышла из системы
        self.wait_to_be_logged_out(email=test_mail)
