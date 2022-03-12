import logging

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Token

logger = logging.getLogger('accounts')


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token={uid}'.format(uid=str(token.uid))
    )
    message_body = 'Use this link to log in:\n\n{url}'.format(url=url)
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
    user = authenticate(uid=request.GET['token'])
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request: HttpRequest):
    auth_logout(request)
    return redirect('/')
