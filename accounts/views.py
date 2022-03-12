import uuid
import logging

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout

from accounts.models import Token

logger = logging.getLogger('accounts')


def send_login_email(request: HttpRequest):
    ''' выслать ссылку на логин по почте'''
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    logger.info(msg=f'saving uid {uid}, for email {email}')
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(subject='Your login link for ToDo lists',
              message=f'Use this link to log in: \n\n{url}',
              from_email='noreply@todolists',
              recipient_list=[email])
    return render(request=request, template_name='accounts/login_email_sent.html')


def login(request: HttpRequest):
    ''' регистрация в системе '''
    logger.info(msg='login view')
    uid = request.GET['uid']
    user = authenticate(uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request: HttpRequest):
    auth_logout(request)
    return redirect('/')
