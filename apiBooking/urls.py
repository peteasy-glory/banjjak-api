# -*- coding: utf-8 -*-

from django.urls import path

from apiBooking.views import api_beauty, api_payment_cusotmer_pet, api_noshow, api_payment_goods, api_grade, api_pet, \
    api_waiting, api_customer_memo, api_join, api_prohibition, api_working_time, api_statutory_holidays, \
    api_payment_memo, api_payment_worker_date, api_payment_time, api_payment_cancel, api_beauty_gallery, \
    api_beauty_sign, api_coupon, api_payment_product, api_payment_discount, api_payment_card_cash, api_payment_confirm, \
    api_payment_coupon, api_hotel
from apiSetting.views import api_schedule_artist

urlpatterns = [
    path('booking/pettype', api_pet.TPetType.as_view()),
    path('booking/b/<str:partner_id>', api_beauty.TBooking.as_view()),
    path('booking/count/<str:partner_id>', api_beauty.TBookingCount.as_view()),
    path('booking/pet-pay/<str:partner_id>', api_beauty.TBookingPetPay.as_view()),
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
    path('booking/payment-memo', api_payment_memo.TMemo.as_view()),

    path('booking/time', api_payment_time.TTime.as_view()),
    path('booking/worker-date', api_payment_worker_date.TWorkerDate.as_view()),
    path('booking/cancel', api_payment_cancel.TCancel.as_view()),
    path('booking/beauty-gallery', api_beauty_gallery.TGallery.as_view()),
    path('booking/beauty-gallery/<int:idx>', api_beauty_gallery.TGallery.as_view()),

    path('booking/beauty-sign', api_beauty_sign.TSign.as_view()),
    path('booking/beauty-sign/<str:partner_id>', api_beauty_sign.TSign.as_view()),

    path('booking/coupon/<str:partner_id>', api_coupon.TCoupon.as_view()),
    path('booking/payment-coupon', api_payment_coupon.TPaymentCoupon.as_view()),
    path('booking/payment-product', api_payment_product.TPaymentProduct.as_view()),
    path('booking/payment-discount', api_payment_discount.TPaymentDiscount.as_view()),
    path('booking/payment-cardcash', api_payment_card_cash.TPaymentCardCash.as_view()),
    path('booking/payment-confirm', api_payment_confirm.TPaymentConfirm.as_view()),



    path('booking/payment-goods/<int:idx>', api_payment_goods.TPaymentGoods.as_view()),
    path('booking/noshow', api_noshow.TNoShow.as_view()),
    path('booking/noshow/<int:idx>', api_noshow.TNoShow.as_view()),
    path('booking/grade-shop', api_grade.TShopGrade.as_view()),
    path('booking/grade/shop', api_grade.TGrade.as_view()),
    path('booking/grade/shop/<str:partner_id>', api_grade.TGrade.as_view()),


    #path('booking/grade-customer/<int:customer_grade_idx>', api_grade.TCustomerGrade.as_view()),
    path('booking/prohibition', api_prohibition.TProhibition.as_view()),
    path('booking/prohibition/<str:partner_id>', api_prohibition.TProhibition.as_view()),
    path('booking/working-time/<str:partner_id>', api_working_time.TWorkingTime.as_view()),
    path('booking/statutory-holidays/<str:partner_id>', api_statutory_holidays.TStatutoryHolidays.as_view()),


    #hotel
    path('booking/h/<str:partner_id>', api_hotel.TBooking.as_view()), #기간별 예약 불러오기
    path('booking/h/join/', api_join.TJoinHotel.as_view()), # 예약하기
    path('booking/hotel-customer-pet/<str:idx>', api_payment_cusotmer_pet.TCustomerPetInfoHotel.as_view()), # 작업/결제관리 불러오기
    path('booking/hotel-before-etc/<str:idx>', api_payment_cusotmer_pet.TCustomerPetInfoHotel.as_view()), # 이전호텔이용 및 이전 특이사항 가져오기
    path('booking/hotel-memo', api_payment_memo.TMemoHotel.as_view()), # 특이사항 수정/등록하기
    path('booking/hotel-noshow', api_noshow.TNoShowHotel.as_view()), # 노쇼 등록/수정하기
    path('booking/time-hotel', api_payment_time.TTimeHotel.as_view()), # 시간변경
    path('booking/date-hotel', api_payment_worker_date.TDateHotel.as_view()), # 날짜변경
    path('booking/pickup-hotel', api_hotel.TPickUp.as_view()),  # 픽업 여부 및 주소 수정하기
    path('booking/payment-hotel', api_hotel.TPayment.as_view()),  # 픽업 여부 및 주소 수정하기


]
