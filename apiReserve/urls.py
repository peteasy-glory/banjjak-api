# -*- coding: utf-8 -*-

from django.urls import path
from apiReserve.views import api_shop_reserve, api_payment_reserve, api_diary
from apiPerformance.views import api_performance

urlpatterns = [

    path('reserve/shop-reserve/<str:partner_id>', api_shop_reserve.TShop.as_view()),
    path('reserve/shop-reserve', api_shop_reserve.TShop.as_view()),
    path('reserve/payment-reserve', api_payment_reserve.TPayment.as_view()),

    path('reserve/diary/<int:idx>', api_diary.TDiary.as_view()),
    path('reserve/diary', api_diary.TDiary.as_view()),
    path('reserve/diary-history', api_diary.TDiaryHistory.as_view()),
    path('reserve/diary-list', api_diary.TDiaryList.as_view()),
    path('reserve/diary-select', api_diary.TDiaryListSelect.as_view()),

]
