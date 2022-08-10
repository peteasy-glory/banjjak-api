# -*- coding: utf-8 -*-

from django.urls import path

from apiCustomer.views import api_total_search, api_sign

urlpatterns = [

    # customer/search/pettester@peteasy.kr?type=beauty
    # customer/search/pettester@peteasy.kr?type=hotel
    # customer/search/pettester@peteasy.kr?type=kinder
    path('customer/search', api_total_search.TTotalSearch.as_view()),
    path('customer/search/<str:partner_id>', api_total_search.TTotalSearch.as_view()),
    path('customer/sign/<str:partner_id>', api_sign.TSign.as_view()),

]