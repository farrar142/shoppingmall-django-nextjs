import json
from datetime import datetime, timedelta
from typing import List, Optional

import requests
from accounts.models import User
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator
from django.db.models import *
from django.http import (HttpRequest, HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, JsonResponse)
from django.shortcuts import render
from ninja import Form, NinjaAPI, Schema, File
from ninja.files import UploadedFile
from ninja.renderers import BaseRenderer
from commons.models import UploadFileModel
from base.serializer import converter
from tokenmiddleware.models import Token
from base.functions import to_dict

from pprint import pprint

from .secret import REDIRECT_URI, REST_API_KEY

accounts_api = NinjaAPI(csrf=False)


class MarketRegisterForm(Schema):
    name: str = ""
    siteUrl: str = ""
    email: str = ""
    desc: str = ""


@accounts_api.post('test')
def test(request, form: MarketRegisterForm = Form(None), file: UploadedFile = File(None)):
    data = file.read()
    print(file.name)
    uploaded: UploadFileModel = UploadFileModel.objects.create(
        title=file.name, file=file)
    print(uploaded.get_url)
    return "hi"


class LoginCheckForm(Schema):
    token: str


def result(res):
    return {
        "result": res
    }


@accounts_api.post("info")
def get_user_info(request, form: LoginCheckForm):
    token: Token = Token.objects.get(token=form.token)
    user: User = token.user
    result = {
        "username": user.username,
        "email": user.email,
        "shop": converter(user.market_set.all())
    }
    return result


@accounts_api.post('check_login')
def check_login(request, form: LoginCheckForm):
    user = Token.objects.filter(token=form.token)
    if user.exists():
        return result(True)
    else:
        return result(False)


@accounts_api.get('kakao_login')
def Kakao_login(request: HttpRequest, browser_id: str):
    kakao_auth_api = "https://kauth.kakao.com/oauth/authorize?"
    return {"url":
            f"{kakao_auth_api}client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code&state={browser_id}"
            }


@accounts_api.get('kakao_callback')
def Kakao_login_callback(request):
    code = request.GET.get("code")
    browser_id = u'kakao_{}'.format(request.GET.get("state"))
    token_request = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
    )

    token_json = token_request.json()

    error = token_json.get("error", None)
    if error is not None:
        raise Exception('카카오 로그인 에러')

    access_token = token_json.get("access_token")

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    id = profile_json.get("id")
    email = profile_json.get("kakao_account").get("email")
    User.login_with_kakao(request, id, email)
    user = User.objects.get(provider_accounts_id=id)
    token = Token.get_valid_token(user.pk)
    print("브라우저 ID in API")
    print(browser_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        browser_id,
        {
            "type": "kakao_login",
            "token": to_dict(token)
        }
    )

    return render(request, 'success.html')
