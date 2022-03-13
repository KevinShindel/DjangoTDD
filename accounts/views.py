import logging
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token

logger = logging.getLogger('accounts')

SUCCESS_SEND_MAIL = "Check your email, we've sent you a link you can use to log in."


def send_login_email(request: HttpRequest):
    ''' выслать ссылку на логин по почте'''
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + f'?uid={token.uid}'
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for ToDo lists',
        message_body,
        'noreply@todolists',
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request: HttpRequest):
    ''' регистрация в системе '''
    logger.info(msg='login view')
    user = auth.authenticate(request.GET['uid'])
    if user is not None:
        auth.login(request, user)
    return redirect('/')


def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('/')
