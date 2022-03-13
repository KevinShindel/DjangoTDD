from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token, User


class AuthTest(TestCase):

    def test_returns_None_if_no_such_user(self):
        ''' тест возвращает пустоту если нет пользователя '''
        result = PasswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_email_if_token_exists(self):
        ''' тест возвращается новый пользователь с почтой если токен существует '''
        email = 'some@mail.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_exist_user_with_email_if_token_exists(self):
        ''' тест возвращается существующий пользователь с правильной электронной почтой если токен существует '''
        email = 'some@mail.com'
        exist_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, exist_user)


class GetUserTest(TestCase):

    def test_get_user_by_email(self):
        ''' тест получает пользователя по адрессу почты '''
        User.objects.create(email='some@mail.com')
        desired_user = User.objects.create(email='another@mail.com')
        found_user = PasswordlessAuthenticationBackend().get_user('another@mail.com')
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self):
        ''' тест возвращает None если нет пользователя с таким email '''
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user('no@mail.com'))
