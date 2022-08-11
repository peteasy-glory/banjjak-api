# -*- coding: utf-8 -*-

from django.urls import path

from apiBooking.views import api_beauty, api_payment_cusotmer_pet, api_noshow, api_payment_goods, api_grade
from apiSetting.views import api_schedule_artist

urlpatterns = [
    path('booking/b/<str:partner_id>', api_beauty.TBooking.as_view()),
    path('booking/b/join/<str:partner_id>', api_beauty.TBookingJoin.as_view()),

    path('booking/schedule-artist/<str:partner_id>', api_schedule_artist.TScheduleArtist.as_view()),
    path('booking/payment-customer-pet/<int:payment_idx>', api_payment_cusotmer_pet.TCustomerPetInfo.as_view()),
    path('booking/payment-before-etc/<int:payment_idx>', api_payment_cusotmer_pet.TCustomerPetInfo.as_view()),
    path('booking/payment-goods/<int:payment_idx>', api_payment_goods.TPaymentGoods.as_view()),
    path('booking/noshow', api_noshow.TNoShow.as_view()),
    path('booking/noshow/<int:payment_idx>', api_noshow.TNoShow.as_view()),

    path('booking/grade-shop', api_grade.TShopGrade.as_view()),
    #path('booking/grade-customer/<int:customer_grade_idx>', api_grade.TCustomerGrade.as_view()),

]
