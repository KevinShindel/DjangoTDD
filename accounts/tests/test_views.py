from django.test import TestCase

from django.http import HttpResponse


class SendLoginEmailViewTest(TestCase):
    ''' тест представление которое отправляет сообщение для входа в систему'''

    def test_redirects_to_tome_page(self):
        ''' тест переадресация на домашнюю страницу '''
        response: HttpResponse = self.client.post('/accounts/send_login_email', data={'email': 'some@mail.com'})
        self.assertRedirects(response, '/')