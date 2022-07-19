# -*- coding: utf-8 -*-

from django.urls import path

from apiLogin.views import api_login, api_join

urlpatterns = [
    path('login', api_login.TLogin.as_view()),
    # path('logout', api_auth_setting.TAuthSetting.as_view()),
    path('join/<str:partner_id>', api_join.TJoin.as_view()),
    path('join', api_join.TJoin.as_view()),
]