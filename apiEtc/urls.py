# -*- coding: utf-8 -*-

from django.urls import path
from apiEtc.views import api_qna
from apiShop.views import api_front, api_info, api_gallery, api_review, api_blog

urlpatterns = [

    path('etc/one-on-one', api_qna.TQna.as_view()),
    path('shop/front/<str:partner_id>', api_front.TFront.as_view()),

]
