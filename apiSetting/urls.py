# -*- coding: utf-8 -*-

from django.urls import path
from apiSetting.views import api_artist_work, api_open_close, api_regular_holiday, api_artist_vacation, api_part_time, \
    api_break_time, api_artist_setting, api_schedule_artist, api_auth_setting, api_reserve, api_pay_type, \
    api_beauty_product, \
    api_beauty_option, api_beauty_coupon, api_etc_product, api_vat, api_product_part, api_product_add_opt, api_shop_vat, \
    api_product_add_opt_etc, api_store_goods, api_coupon
from apiSetting.views.hotel import api_h_product, api_hotel
from apiSetting.views.kindergarden import api_kindergarden, api_k_product

urlpatterns = [

    path('setting/schedule-mgr/<str:partner_id>', api_schedule_artist.TScheduleArtist.as_view()),
    path('setting/working', api_artist_work.TArtistWork.as_view()),
    path('setting/working/<str:partner_id>', api_artist_work.TArtistWork.as_view()),
    path('setting/break-time', api_break_time.TBreakTime.as_view()),
    path('setting/break-time/<str:partner_id>', api_break_time.TBreakTime.as_view()),
    path('setting/part-time', api_part_time.TPartTime.as_view()),
    path('setting/part-time/<str:partner_id>', api_part_time.TPartTime.as_view()),
    path('setting/part-time-set', api_part_time.TPartTimeSet.as_view()),
    path('setting/part-time-set/<str:partner_id>', api_part_time.TPartTimeSet.as_view()),
    path('setting/artist-vacation', api_artist_vacation.TVacation.as_view()),
    path('setting/artist-vacation/<str:partner_id>', api_artist_vacation.TVacation.as_view()),
    path('setting/open-close', api_open_close.TOpenClose.as_view()),
    path('setting/open-close/<str:partner_id>', api_open_close.TOpenClose.as_view()),
    path('setting/regular-holiday', api_regular_holiday.TReqularHoliday.as_view()),
    path('setting/regular-holiday/<str:partner_id>', api_regular_holiday.TReqularHoliday.as_view()),
    path('setting/artist-put', api_artist_setting.TAuthSetting.as_view()),
    path('setting/out-artist', api_artist_setting.TArtistOut.as_view()),
    path('setting/view-artist', api_artist_setting.TArtistView.as_view()),
    path('setting/ord-artist', api_artist_setting.TArtistOrd.as_view()),
    path('setting/is-authority/<str:partner_id>', api_auth_setting.TAuthSetting.as_view()),
    path('setting/authority', api_auth_setting.TAuthSetting.as_view()),
    path('setting/authority/<str:partner_id>', api_auth_setting.TAuthView.as_view()),
    path('setting/reserve/<str:partner_id>', api_reserve.TReserve.as_view()),
    path('setting/reserve', api_reserve.TReserve.as_view()),
    path('setting/pay-type/<str:partner_id>', api_pay_type.TPayType.as_view()),
    path('setting/pay-type', api_pay_type.TPayType.as_view()),
    path('setting/beauty-product/<str:partner_id>', api_beauty_product.TProduct.as_view()),
    path('setting/option-product/<str:partner_id>', api_beauty_option.TProduct.as_view()),
    path('setting/b/product/part/dog/<str:partner_id>', api_product_part.TDog.as_view()),
    path('setting/b/product/part/dog', api_product_part.TDog.as_view()),
    path('setting/b/product/part-time/dog', api_product_part.TPartTime.as_view()),
    path('setting/b/product/add-opt/kind/<str:partner_id>', api_product_add_opt.TKind.as_view()),
    path('setting/b/product/add-opt/dog', api_product_add_opt.TDog.as_view()),
    path('setting/b/product/add-opt/dog/<str:partner_id>', api_product_add_opt.TDog.as_view()),
    path('setting/b/product/add-opt-etc/dog', api_product_add_opt_etc.TDog.as_view()),
    path('setting/shop-vat/<str:partner_id>', api_shop_vat.TShopVat.as_view()),
    path('setting/shop-vat', api_shop_vat.TShopVat.as_view()),
    path('setting/beauty-coupon/<str:partner_id>', api_beauty_coupon.TCoupon.as_view()),
    path('setting/beauty-coupon', api_beauty_coupon.TCoupon.as_view()),
    path('setting/beauty-coupon-memo', api_beauty_coupon.TCouponMemo.as_view()),
    path('setting/etc-product/<str:partner_id>', api_etc_product.TProduct.as_view()),
    path('setting/vat', api_vat.TAPIVat.as_view()),
    path('setting/vat/<str:partner_id>', api_vat.TAPIVat.as_view()),
    path('setting/beauty-store-goods', api_store_goods.TGoods.as_view()),
    #===============
    path('setting/hotel/<str:partner_id>', api_hotel.THotel.as_view()),
    path('setting/hotel', api_hotel.THotel.as_view()),
    path('setting/hotel-product/<str:partner_id>', api_h_product.TRoom.as_view()),
    path('setting/hotel-product', api_h_product.TRoom.as_view()),

    path('setting/kindergarden/<str:partner_id>', api_kindergarden.TKindergarden.as_view()),
    path('setting/kindergarden', api_kindergarden.TKindergarden.as_view()),
    path('setting/kindergarden-product/<str:partner_id>', api_k_product.TRoom.as_view()),
    path('setting/kindergarden-product', api_k_product.TRoom.as_view()),

    ## 중복됨 -- 미용 쿠폰 api를 사용할 것
    path('setting/coupon/<str:partner_id>', api_coupon.TCoupon.as_view()),
    path('setting/coupon', api_coupon.TCoupon.as_view()),
    #=======================================================================
]