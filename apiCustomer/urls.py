# -*- coding: utf-8 -*-

from django.urls import path

from apiCustomer.views import api_total_search, api_sign, api_usage_history, api_petlist, api_unique_memo, api_reserves, \
    api_user, api_subphone, api_phone_history

urlpatterns = [

    # customer/search/pettester@peteasy.kr?type=beauty
    # customer/search/pettester@peteasy.kr?type=hotel
    # customer/search/pettester@peteasy.kr?type=kinder
    path('customer/search', api_total_search.TTotalSearch.as_view()),
    path('customer/search/<str:partner_id>', api_total_search.TTotalSearch.as_view()),
    path('customer/sign/<str:partner_id>', api_sign.TSign.as_view()),

    path('customer/usage-history/<str:partner_id>', api_usage_history.TUsageHistory.as_view()),
    path('customer/petlist/<str:partner_id>', api_petlist.TPetList.as_view()),
    path('customer/pet', api_petlist.TPetList.as_view()),
    path('customer/user', api_user.TUser.as_view()),
    path('customer/unique-memo/<str:partner_id>', api_unique_memo.TUniqueMemo.as_view()),
    path('customer/reserves/<str:partner_id>', api_reserves.TReserves.as_view()),

    path('customer/subphone', api_subphone.TSubPhone.as_view()),
    path('customer/subphone/<str:partner_id>', api_subphone.TSubPhone.as_view()),
    path('customer/phone-change', api_phone_history.TMainPhone.as_view()),
    path('customer/phone-change/<str:partner_id>', api_phone_history.TMainPhone.as_view()),
]