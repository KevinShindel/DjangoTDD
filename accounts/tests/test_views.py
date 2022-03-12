from itertools import repeat
from unittest.mock import patch, Mock, call

from django.test import TestCase
from django.urls import reverse

from accounts.views import SUCCESS_SEND_MAIL


class SendLoginEmailViewTest(TestCase):
    ''' тест представление которое отправляет сообщение для входа в систему'''

    def setUp(self) -> None:
        self.send_mail_called, self.subject, self.body, self.from_email, self.to_email = repeat(None, 5)

    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    # def test_sends_mail_to_address_from_post(self):
    #     '''тест отправляется сообщение на адрес из метода post '''
    #     self.send_mail_called = False
    #
    #     def fake_send_mail(subject, body, from_email, to_email):
    #         ''' поддельная функция send_mail '''
    #         self.send_mail_called = True
    #         self.subject = subject
    #         self.body = body
    #         self.from_email = from_email
    #         self.to_email = to_email
    #
    #     accounts.views.send_mail = fake_send_mail
    #
    #     self.client.post(reverse('send_login_email'), data={'email': 'some@mail.com'})
    #     self.assertTrue(self.send_mail_called)
    #     self.assertEqual(self.subject, 'Your login link for To Do lists')
    #     self.assertEqual(self.from_email, 'noreply@todolists')
    #     self.assertEqual(self.to_email, ['some@mail.com'])

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail: Mock):
        '''тест отправляется сообщение на адрес из метода post '''
        self.client.post(reverse('send_login_email'), data={'email': 'some@mail.com'})
        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), _ = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for ToDo lists')
        self.assertEqual(from_email, 'noreply@todolists')
        self.assertEqual(to_list, ['some@mail.com'])

    # def test_adds_success_message(self):
    #     ''' тест добавляется сообщение об успехе '''
    #     response = self.client.post(reverse('send_login_email'), data={'email': 'some@mail.com'}, follow=True)
    #     message = list(response.context['messages'])[0]
    #     self.assertEqual(message.message, SUCCESS_SEND_MAIL)
    #     self.assertEqual(message.tags, "success")

    @patch('accounts.views.messages')
    def test_adds_success_messages_with_mocks(self, mock_messages):
        response = self.client.post(reverse('send_login_email'), data={'email': 'some@mail.com'})
        self.assertEqual(mock_messages.success.call_args, call(response.wsgi_request, SUCCESS_SEND_MAIL))


