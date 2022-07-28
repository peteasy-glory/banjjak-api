# -*- coding: utf-8 -*-

from django.urls import path

from apiBooking.views import api_beauty

urlpatterns = [
    path('booking/b/<str:partner_id>', api_beauty.TBooking.as_view()),
]
