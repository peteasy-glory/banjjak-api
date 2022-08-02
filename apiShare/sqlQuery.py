# -*- coding: utf-8 -*-

#Login Logout Join etc...
PROC_LOGIN_GET = "call procPartnerPC_LogIn_get('%s', '%s')"
PROC_LOGIN_ARTIST_GET = "call procPartnerPC_LogIn_Artist_get('%s')"

PROC_IS_EXIST_ID_GET = "call procPartnerPC_Is_Exist_Id_get('%s')"
PROC_JOIN_POST = "call procPartnerPC_Join_post('%s','%s','%s','%s')"
PROC_IS_EXIST_PHONE_GET = "call procPartnerPC_Is_Exist_Phone_get('%s')"

#Home
PROC_SHOP_NAME_GET = "call procPartnerPC_ShopName_get('%s')"
PROC_TOP_INFO_GET= "call procPartnerPC_Home_TopInfo_get('%s', %s, %s, %s)"
PROC_SPETIAL_MALL_GET= "call procPartnerPC_Home_SpetialMall_get()"
PROC_CONSULT_MGR_GET= "call procPartnerPC_Home_ConsultinMgr_get('%s')"
PROC_NOTICE_MGR_GET= "call procPartnerPC_Home_NoticeMgr_get(%s, '%s', '%s')"
PROC_BEAUTY_BOOKING_GET= "call procPartnerPC_Home_BeautyBookingMgr_get('%s', %s, %s)"
PROC_HOTEL_BOOKING_GET= "call procPartnerPC_Home_HotelBookingMgr_get('%s', %s, %s)"
PROC_KINDERGADEN_BOOKING_GET= "call procPartnerPC_Home_KindergardenBookingMgr_get('%s', %s, %s)"
PROC_CELLPHONE_SEARCH_GET= "call procPartnerPC_Home_PhoneSearch_get('%s', '%s')"


#BOOKING
PROC_BEAUTY_BOOKING_PEROID_GET = "call procPartnerPC_Booking_BeautyPeroid_get('%s', '%s', '%s')"
PROC_BEAUTY_BOOKING_CUSTOMER_PET_INFO_GET = "call procPartnerPC_Booking_CustomerPetInfo_get(%s)"
PROC_BEAUTY_BOOKING_BEFORE_PAYMENT_INFO_GET = "call procPartnerPC_Booking_BeforePaymentInfo_get(%s, %s, %s)"


#AUTH SETTING

PROC_SETTING_ARTIST_POST = "call procPartnerPC_Setting_Artist_post('%s', '%s', '%s', '%s', '%s', '%s', %s, '%s', '%s', %s)"

PROC_SETTING_ARTIST_WORKING_GET = "call procPartnerPC_Setting_Artist_Working_get('%s')"
PROC_SETTING_SHOP_OPEN_CLOSE_GET = "call procPartnerPC_Setting_Shop_OpenClose_get('%s')"
PROC_SETTING_REGULAR_HOLIDAY_GET = "call procPartnerPC_Setting_Regular_Holiday_get('%s')"
PROC_SETTING_PERSONAL_VACATION_GET = "call procPartnerPC_Setting_Personal_Vacation_get('%s')"
PROC_SETTING_TIME_LIMIT_GET = "call procPartnerPC_Setting_Time_Limit_get('%s')"
PROC_SETTING_BREAK_TIME_GET = "call procPartnerPC_Setting_Break_Time_get('%s')"


