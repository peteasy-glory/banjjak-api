# -*- coding: utf-8 -*-

#Login Logout Join etc...
PROC_LOGIN_GET = "call procPartnerPC_LogIn_get('%s', '%s')"
PROC_LOGIN_ARTIST_GET = "call procPartnerPC_LogIn_Artist_get('%s')"

PROC_IS_EXIST_ID_GET = "call procPartnerPC_Is_Exist_Id_get('%s')"
PROC_JOIN_POST = "call procPartnerPC_Join_post('%s','%s','%s','%s')"
PROC_IS_EXIST_PHONE_GET = "call procPartnerPC_Is_Exist_Phone_get('%s')"
PROC_WORKER_TO_CEO_GET = "call procPartnerPC_Login_Ceo_get('%s')"

#Home
PROC_NAVIGATION_INFO_GET= "call procPartnerPC_Navigation_Info_get('%s')"
PROC_SHOP_NAME_GET = "call procPartnerPC_ShopName_get('%s')"
PROC_TOP_INFO_GET= "call procPartnerPC_Home_TopInfo_get('%s', %s, %s, %s)"
PROC_SPETIAL_MALL_GET= "call procPartnerPC_Home_SpetialMall_get()"
PROC_CONSULT_MGR_GET= "call procPartnerPC_Home_ConsultinMgr_get('%s')"
PROC_CONSULT_PHOTO_GET= "call procPartnerPC_Home_ConsultingPhoto_get(%s)"
PROC_NOTICE_MGR_GET= "call procPartnerPC_Home_NoticeMgr_get(%s, '%s', '%s')"
PROC_BEAUTY_BOOKING_GET= "call procPartnerPC_Home_BeautyBookingMgr_get('%s', %s, %s)"
PROC_HOTEL_BOOKING_GET= "call procPartnerPC_Home_HotelBookingMgr_get('%s', %s, %s)"
PROC_KINDERGADEN_BOOKING_GET= "call procPartnerPC_Home_KindergardenBookingMgr_get('%s', %s, %s)"

PROC_CELLPHONE_SEARCH_GET = "call procPartnerPC_Home_PhoneSearch_get('%s', '%s')"
PROC_SEARCH_PHONE_GET = "call procPartnerPC_Home_SearchPhone_get('%s', '%s')"
PROC_SEARCH_PET_NAME_GET = "call procPartnerPC_Home_SearchPetName_get('%s', '%s')"
PROC_CONSULT_BOOKING_WAITING_COUNT_GET = "call procPartnerPC_Home_WaitingCount_get('%s')"

PROC_NO_SHOW_COUNT_GET = "call procPartnerPC_Home__NoShowCount_get('%s','%s')"


#BOOKING
PROC_BEAUTY_BOOKING_PEROID_GET = "call procPartnerPC_Booking_BeautyPeroid_get('%s', '%s', '%s')"
PROC_BEAUTY_BOOKING_CUSTOMER_PET_INFO_GET = "call procPartnerPC_Booking_CustomerPetInfo_get(%s)"
PROC_BEAUTY_BOOKING_BEFORE_PAYMENT_INFO_GET = "call procPartnerPC_Booking_BeforePaymentInfo_get(%s, %s, %s)"
PROC_BEAUTY_BOOKING_PAYMENT_INFO_GET = "call procPartnerPC_Booking_PaymentInfo_get(%s)"
PROC_BEAUTY_BOOKING_PAYMENT_MEMO_PUT = "call procPartnerPC_Booking_PaymentInfoEtcMemo_put(%d, '%s')"
PROC_BEAUTY_BOOKING_NO_SHOW_PUT = "call procPartnerPC_Booking_NoShow_put(%s, %s)"
PROC_BEAUTY_BOOKING_TIME_PUT = "call procPartnerPC_Booking_Time_put(%d, '%s', '%s')"
PROC_BEAUTY_BOOKING_DATE_WORKER_PUT = "call procPartnerPC_Booking_DateWorker_put(%d, '%s','%s','%s')"
PROC_BEAUTY_BOOKING_CANCEL_PUT = "call procPartnerPC_Booking_Cancel_put(%d, %d)"
PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_GET = "call procPartnerPC_Booking_BeautyGallery_get(%d)"
PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_POST = "call procPartnerPC_Booking_BeautyGallery_post(%d,'%s', %d, '%s','%s')"
PROC_BEAUTY_BOOKING_BEAUTY_GALLERY_DELETE = "call procPartnerPC_Booking_BeautyGallery_delete(%d)"
PROC_BEAUTY_BOOKING_BEAUTY_SIGN_GET = "call procPartnerPC_Booking_BeautySign_get('%s',%d)"
PROC_BEAUTY_BOOKING_BEAUTY_SIGN_POST = "call procPartnerPC_Booking_BeautySign_post('%s','%s','%s', %d, '%s','%s','%s','%s','%s','%s')"


PROC_BEAUTY_BOOKING_COUPON_GET = "call procPartnerPC_Booking_Coupon_get('%s', '%s', '%s')"
PROC_BEAUTY_BOOKING_BEAUTY_PRODUCT_POST = "call procPartnerPC_Booking_BeautySign_post('%s','%s','%s', %d, '%s','%s','%s','%s','%s','%s')"





PROC_BEAUTY_BOOKING_GRADE_SHOP_ID_GET = "call procPartnerPC_Booking_GRADE_SHOP_ID_get('%s')"
PROC_BEAUTY_BOOKING_GRADE_SHOP_IDX_GET = "call procPartnerPC_Booking_GRADE_SHOP_IDX_get(%s)"
PROC_BEAUTY_BOOKING_GRADE_CUSTOMER_POST = "call procPartnerPC_Booking_GradeCustomer_post(%s, %s,'%s')"
PROC_BEAUTY_BOOKING_GRADE_CUSTOMER_PUT = "call procPartnerPC_Booking_GradeCustomer_put(%s, %s, '%s')"
PROC_BEAUTY_BOOKING_GRADE_SHOP_PUT = "call procPartnerPC_Booking_ShopGrade_put(%s, '%s')"
PROC_BEAUTY_BOOKING_PET_TYPE_GET = "call procPartnerPC_Booking_PetType_get('%s')"
PROC_BEAUTY_BOOKING_PREDATA_STATIC_GET = "call procPartnerPC_Booking_PreDataStatic_get('%s')"
PROC_BEAUTY_BOOKING_PREDATA_COMMON_GET = "call procPartnerPC_Booking_PreDataCommon_get('%s')"
PROC_BEAUTY_BOOKING_PREDATA_WORKTIME_GET = "call procPartnerPC_Booking_PreDataWorktime_get('%s')"
PROC_BEAUTY_BOOKING_PREDATA_COMMON_OPTION_GET = "call procPartnerPC_Booking_PreDataCommOption_get('%s')"
PROC_BEAUTY_BOOKING_SOHP_INFO_GET = "call procPartnerPC_Booking_ShopInFo_get('%s')"

PROC_BEAUTY_BOOKING_PREDATA_CAT_GET = "call procPartnerPC_Booking_PreDataCat_get('%s')"
PROC_BEAUTY_BOOKING_WAITING_LIST_GET = "call procPartnerPC_Booking_WaitingList_get('%s')"
PROC_BEAUTY_BOOKING_WAITING_DECISION_PUT = "call procPartnerPC_Booking_Decision_put(%d,%d,%d)"
PROC_BEAUTY_BOOKING_CUSTOMER_MEMO_GET = "call procPartnerPC_Booking_CustomerMemo_get('%s','%s','%s','%s')"
PROC_BEAUTY_BOOKING_CUSTOMER_MEMO_PUT = "call procPartnerPC_Booking_CustomerMemo_put(%d,'%s')"
PROC_BEAUTY_BOOKING_PET_INFO_GET = "call procPartnerPC_Booking_PetInfo_get(%d)"
PROC_BEAUTY_BOOKING_PET_INFO_PUT = "call procPartnerPC_Booking_PetInfo_put(%d,'%s','%s','%s',%d,%d,%d,'%s',%d,'%s'," \
                                   "'%s','%s','%s','%s',%d,%d,%d,%d,'%s')"
PROC_BEAUTY_BOOKING_POST = "call procPartnerPC_Booking_post('%s','%s','%s','%s',%d,'%s','%s','%s',%d, %d, %d,'%s'," \
                           "'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d, %d, %d,%d, %d,'%s','%s','%s','%s'," \
                           "'%s','%s',%d,%d,'%s','%s','%s','%s','%s')"

PROC_BEAUTY_BOOKING_PROHIBITION_GET = "call procPartnerPC_Booking_Prohibition_get('%s','%s','%s');"
PROC_BEAUTY_BOOKING_PROHIBITION_POST = "call procPartnerPC_Booking_Prohibition_post('%s','%s','%s','%s','%s');"
PROC_BEAUTY_BOOKING_PROHIBITION_DELETE = "call procPartnerPC_Booking_Prohibition_delete(%d);"

PROC_BEAUTY_BOOKING_SHOP_WORKING_TIME_GET = "call procPartnerPC_Booking_ShopWorkingTime_get('%s')"
PROC_BEAUTY_BOOKING_STATUTORY_HOLIDAYS_GET = "call procPartnerPC_Booking_StatutoryHolidays_get(%d, %d)"


#CUSTOMER MGR
PROC_CUSTOMER_TOTAL_COUNT_GET = "call procPartnerPC_CustomerTotalCount_get('%s')"
PROC_ANIMAL_TOTAL_COUNT_GET = "call procPartnerPC_AnimalTotalCount_get('%s')"
PROC_CUSTOMER_BEAUTY_TOTAL_SEARCH_GET = "call procPartnerPC_BeautyCutomerSearchTotal_get('%s', %s, %s, %s)"
PROC_CUSTOMER_HOTEL_TOTAL_SEARCH_GET = "call procPartnerPC_HotelCutomerSearchTotal_get('%s', %s, %s, %s)"
PROC_CUSTOMER_KINDER_TOTAL_SEARCH_GET = "call procPartnerPC_KinderCutomerSearchTotal_get('%s', %s, %s, %s)"
PROC_CUSTOMER_BEAUTY_AGREE_GET = "call procPartnerPC_BeautyAgree_get('%s', %s)"
PROC_CUSTOMER_JOIN_POST = "call procPartnerPC_CustomerJoin_post('%s','%s','%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"

#SHOP MGE
PROC_SHOP_FRONT_IMAGE_GET = "call procPartnerPC_Shop_Front_get('%s')"
PROC_SHOP_FRONT_IMAGE_POST = "call procPartnerPC_Shop_Front_post('%s', '%s')"
PROC_SHOP_FRONT_IMAGE_PUT = "call procPartnerPC_Shop_Front_put('%s', '%s')"
PROC_SHOP_FRONT_IMAGE_DELETE = "call procPartnerPC_Shop_Front_delete('%s', '%s')"

PROC_SHOP_INFO_BASE_GET = "call procPartnerPC_Shop_InfoBase_get('%s')"
PROC_SHOP_INFO_PUT = "call procPartnerPC_Shop_Info_put('%s',%d,'%s','%s','%s','%s','%s')"
PROC_SHOP_INFO_PHOTO_PUT = "call procPartnerPC_Shop_InfoPhoto_put('%s','%s')"
PROC_SHOP_INFO_SALES_AREA_GET = "call procPartnerPC_Shop_InfoSalesArea_get('%s')"
PROC_SHOP_INFO_SALES_AREA_POST = "call procPartnerPC_Shop_InfoSalesArea_post('%s', %d)"
PROC_SHOP_INFO_SALES_AREA_DELETE = "call procPartnerPC_Shop_InfoSalesArea_delete('%s', %d)"
PROC_SHOP_INFO_AREA_ADDR_GET = "call procPartnerPC_Shop_AreaAddr_get('%s', '%s')"
PROC_SHOP_INFO_LICENSE_AWARD_GET = "call procPartnerPC_Shop_InfoLicenseAward_get('%s',%d)"
PROC_SHOP_INFO_LICENSE_AWARD_POST = "call procPartnerPC_Shop_InfoLicenseAward_get_post('%s',%d,'%s','%s','%s','%s')"
PROC_SHOP_INFO_LICENSE_AWARD_DELETE = "call procPartnerPC_Shop_InfoLicenseAward_get_delete('%s',%d,'%s')"

PROC_SHOP_GALLERY_GET = "call procPartnerPC_Shop_Gallery_get('%s')"
PROC_SHOP_GALLERY_POST = "call procPartnerPC_Shop_Gallery_post('%s','%s')"
PROC_SHOP_GALLERY_DELETE = "call procPartnerPC_Shop_Gallery_delete(%d)"

PROC_SHOP_REVIEW_GET = "call procPartnerPC_Shop_Review_get('%s')"
PROC_SHOP_REVIEW_PUT = "call procPartnerPC_Shop_Review_put(%d,'%s')"
PROC_SHOP_REVIEW_DELETE = "call procPartnerPC_Shop_Review_delete(%d)"

PROC_SHOP_BLOG_GET = "call procPartnerPC_Shop_Blog_get('%s')"
PROC_SHOP_BLOG_POST = "call procPartnerPC_Shop_Blog_post('%s','%s','%s','%s','%s','%s','%s')"
PROC_SHOP_BLOG_PUT = "call procPartnerPC_Shop_Blog_put(%d,'%s','%s','%s','%s','%s','%s')"
PROC_SHOP_BLOG_DELETE = "call procPartnerPC_Shop_Blog_delete(%d)"


#AUTH SETTING
PROC_SETTING_ARTIST_PUT = "call procPartnerPC_Setting_The_Artist_put('%s', '%s', '%s', '%s', '%s', '%s', '%s', " \
                              "%s, '%s','%s', %s) "
PROC_SETTING_ARTIST_OUT_PUT = "call procPartnerPC_Setting_Artist_Out_put('%s', '%s', '%s')"
PROC_SETTING_ARTIST_VIEW_PUT = "call procPartnerPC_Setting_Artist_View_put('%s', '%s', '%s')"
PROC_SETTING_ARTIST_ORD_PUT = "call procPartnerPC_Setting_Artist_Ord_put('%s', '%s', %s)"
PROC_SETTING_ARTIST_WORKING_GET = "call procPartnerPC_Setting_Artist_Working_get('%s')"
PROC_SETTING_ARTIST_WORKING_POST = "call procPartnerPC_Setting_Artist_Working_post('%s')"

PROC_SETTING_SHOP_OPEN_CLOSE_GET = "call procPartnerPC_Setting_Shop_OpenClose_get('%s')"
PROC_SETTING_SHOP_OPEN_CLOSE_MODIFY = "call procPartnerPC_Setting_Shop_OpenClose_modify('%s',%d,%d,%d)"
PROC_SETTING_REGULAR_HOLIDAY_GET = "call procPartnerPC_Setting_Regular_Holiday_get('%s')"
PROC_SETTING_REGULAR_HOLIDAY_MODIFY = "call procPartnerPC_Setting_Regular_Holiday_modify('%s','%s')"
PROC_SETTING_PERSONAL_VACATION_GET = "call procPartnerPC_Setting_Personal_Vacation_get('%s')"
PROC_SETTING_PERSONAL_VACATION_POST = "call procPartnerPC_Setting_Personal_Vacation_post('%s','%s','%s','%s','%s')"
PROC_SETTING_PERSONAL_VACATION_DELETE = "call procPartnerPC_Setting_Personal_Vacation_delete('%s','%s','%s','%s','%s')"
PROC_SETTING_TIME_LIMIT_GET = "call procPartnerPC_Setting_Time_Limit_get('%s')"
PROC_SETTING_TIME_LIMIT_MODIFY = "call procPartnerPC_Setting_Time_Limit_modify(%d, '%s', '%s', '%s')"
PROC_SETTING_BREAK_TIME_GET = "call procPartnerPC_Setting_Break_Time_get('%s')"
PROC_SETTING_BREAK_TIME_MODIFY = "call procPartnerPC_Setting_Break_Time_modify('%s','%s')"
PROC_IS_EXIST_AUTHORITY_GET = "call procPartnerPC_Is_Exist_Authority_get('%s')"
PROC_SETTING_AUTHORITY_PUT = "call procPartnerPC_Setting_Authority_put('%s', '%s', '%s', '%s')"
PROC_SETTING_AUTHORITY_GET = "call procPartnerPC_Setting_Authority_get('%s')"
PROC_SETTING_RESERVE_GET = "call procPartnerPC_Setting_Reserve_get('%s')"
PROC_SETTING_RESERVE_PUT = "call procPartnerPC_Setting_Reserve_put('%s', '%s', '%s', %s, '%s')"
PROC_SETTING_PAY_TYPE_GET = "call procPartnerPC_Setting_Pay_Type_get('%s')"
PROC_SETTING_PAY_TYPE_PUT = "call procPartnerPC_Setting_Pay_Type_put('%s',%s)"
PROC_SETTING_VAT_GET = "call procPartnerPC_Setting_Vat_get('%s')"
PROC_SETTING_VAT_PUT = "call procPartnerPC_Setting_Vat_put('%s',%d)"
PROC_SETTING_WORKTIME_GET = "call procPartnerPC_Setting_Worktime_get('%s')"
PROC_SETTING_DOG_PRODUCT_GET = "call procPartnerPC_Setting_Dog_Product_get('%s')"
PROC_SETTING_CAT_PRODUCT_GET = "call procPartnerPC_Setting_Cat_Product_get('%s')"
PROC_SETTING_OPTION_PRODUCT_GET = "call procPartnerPC_Setting_Option_Product_get('%s')"
PROC_SETTING_PLUS_OPTION_PRODUCT_GET = "call procPartnerPC_Setting_Plus_Option_Product_get('%s')"
PROC_SETTING_BEAUTY_COUPON_GET = "call procPartnerPC_Setting_Beauty_Coupon_get('%s')"
PROC_SETTING_ETC_PRODUCT_GET = "call procPartnerPC_Setting_Etc_Product_get('%s')"

#ETC
PROC_ETC_ONE_ON_ONE_INQUIRY_GET = "call procPartnerPC_Etc_OneOnOneInquiry_get('%s')"
PROC_ETC_ONE_ON_ONE_INQUIRY_POST= "call procPartnerPC_Etc_OneOnOneInquiry_post('%s','%s','%s','%s','%s','%s')"
PROC_ETC_NOTICE_GET= "call procPartnerPC_Etc_Notice_get()"
PROC_ETC_RESIGN_PUT = "call procPartnerPC_Etc_Resign_put('%s')"
PROC_ETC_PASSWORD_GET = "call procPartnerPC_Etc_Password_get('%s')"
PROC_ETC_PASSWORD_PUT = "call procPartnerPC_Etc_Password_put('%s', '%s')"

PROC_ETC_SALES_PERFORMANCE = "call procPartnerPC_Sales_Performance_get('%s','%s','%s','%s','%s')"