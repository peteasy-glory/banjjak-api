# -*- coding: utf-8 -*-

from django.urls import path

from apiHome.views import api_home

urlpatterns = [
    path('home/<str:partner_id>', api_home.THome.as_view()),
    path('home/<int:year>/<int:month>/<str:partner_id>', api_home.THome.as_view()),

]