# -*- coding: utf-8 -*-

from django.urls import path
from apiReserve.views import api_shop_reserve
from apiPerformance.views import api_performance

urlpatterns = [

    path('reserve/shop-reserve/<str:partner_id>', api_shop_reserve.TShop.as_view()),
    path('reserve/shop-reserve', api_shop_reserve.TShop.as_view()),

]
