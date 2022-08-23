# -*- coding: utf-8 -*-

from django.urls import path

from apiBooking.views import api_beauty, api_payment_cusotmer_pet, api_noshow, api_payment_goods, api_grade, api_pet, \
    api_waiting, api_customer_memo, api_join, api_prohibition, api_working_time, api_statutory_holidays
from apiSetting.views import api_schedule_artist

urlpatterns = [
    path('booking/pettype', api_pet.TPetType.as_view()),
    path('booking/b/<str:partner_id>', api_beauty.TBooking.as_view()),
#    path('booking/join', api_join.TJoin.as_view()),
    path('booking/b/join/', api_join.TJoin.as_view()),
    path('booking/b/join/<str:partner_id>', api_join.TBookingJoin.as_view()),
    path('booking/waiting', api_waiting.TBookingWaiting.as_view()),
    path('booking/waiting/<str:partner_id>', api_waiting.TBookingWaiting.as_view()),
    path('booking/customer-memo', api_customer_memo.TCustomerMemo.as_view()),
    path('booking/customer-memo/<str:partner_id>', api_customer_memo.TCustomerMemo.as_view()),
    path('booking/pet/<int:idx>', api_pet.TPetInfo.as_view()),
    path('booking/pet', api_pet.TPetInfo.as_view()),
    path('booking/schedule-artist/<str:partner_id>', api_schedule_artist.TScheduleArtist.as_view()),
    path('booking/payment-customer-pet/<int:idx>', api_payment_cusotmer_pet.TCustomerPetInfo.as_view()),
    path('booking/payment-before-etc/<int:idx>', api_payment_cusotmer_pet.TCustomerPetInfo.as_view()),
    path('booking/payment-goods/<int:idx>', api_payment_goods.TPaymentGoods.as_view()),
    path('booking/noshow', api_noshow.TNoShow.as_view()),
    path('booking/noshow/<int:idx>', api_noshow.TNoShow.as_view()),
    path('booking/grade-shop', api_grade.TShopGrade.as_view()),
    #path('booking/grade-customer/<int:customer_grade_idx>', api_grade.TCustomerGrade.as_view()),
    path('booking/prohibition', api_prohibition.TProhibition.as_view()),
    path('booking/prohibition/<str:partner_id>', api_prohibition.TProhibition.as_view()),
    path('booking/working-time/<str:partner_id>', api_working_time.TWorkingTime.as_view()),
    path('booking/statutory-holidays/<str:partner_id>', api_statutory_holidays.TStatutoryHolidays.as_view()),

]
