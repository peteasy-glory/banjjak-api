# -*- coding: utf-8 -*-

from django.urls import path
from apiEtc.views import api_qna, api_notice, api_account

urlpatterns = [

    path('etc/one-on-one', api_qna.TQna.as_view()),
    path('etc/one-on-one/<str:partner_id>', api_qna.TQna.as_view()),
    path('etc/notice/<str:partner_id>', api_notice.TNotice.as_view()),
    path('etc/resign', api_account.TResign.as_view()),
    path('etc/pw', api_account.TPassword.as_view()),
    path('etc/pw/<str:partner_id>', api_account.TPassword.as_view()),


]
