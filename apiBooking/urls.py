# -*- coding: utf-8 -*-

from django.urls import path

from apiBooking.views import api_booking

urlpatterns = [
    path('booking/<str:partner_id>', api_booking.TBooking.as_view()),
]
