

# -*- coding: utf-8 -*-

from django.urls import path
from apiAllim.views import api_allim

urlpatterns = [
    path('allim/send', api_allim.TSend.as_view()),
]
