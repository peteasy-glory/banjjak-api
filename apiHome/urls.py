# -*- coding: utf-8 -*-

from django.urls import path

from apiHome.views import api_home

urlpatterns = [
    path('home/<str:partner_id>', api_home.THome.as_view()),
    path('home/<int:year>/<int:month>/<str:partner_id>', api_home.THome.as_view()),
    path('home/search/<str:partner_id>', api_home.TCellSearch.as_view()),
    path('home/consulting/', api_home.TConsultModify.as_view()),
    path('home/consulting/<str:partner_id>', api_home.TConsulting.as_view()),
    path('home/waiting/<str:partner_id>', api_home.TConsultBookingWaiting.as_view()),
    path('home/navigation/<str:partner_id>', api_home.TNavigation.as_view()),


]