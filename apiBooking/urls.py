# -*- coding: utf-8 -*-

from django.urls import path

from apiBooking.views import api_beauty, api_payment_cusotmer_pet
from apiSetting.views import api_schedule_artist

urlpatterns = [
    path('booking/b/<str:partner_id>', api_beauty.TBooking.as_view()),
    path('booking/schedule-artist/<str:partner_id>', api_schedule_artist.TScheduleArtist.as_view()),
    path('booking/payment-customer-pet/<int:payment_idx>', api_payment_cusotmer_pet.TCustomerPetInfo.as_view()),
    path('booking/payment-before-etc/<int:payment_idx>', api_payment_cusotmer_pet.TCustomerPetInfo.as_view()),

]
