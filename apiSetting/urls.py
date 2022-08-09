# -*- coding: utf-8 -*-

from django.urls import path
from apiSetting.views import api_artist_work, api_open_close, api_regular_holiday, api_artist_vacation, api_part_time, \
    api_break_time, api_artist_setting, api_schedule_artist, api_auth_setting
# from apiSetting.views import api_artist_work, api_schedule_artist


urlpatterns = [

    path('setting/schedule-mgr/<str:partner_id>', api_schedule_artist.TScheduleArtist.as_view()),
    path('setting/working/<str:partner_id>', api_artist_work.TArtistWork.as_view()),
    path('setting/open-close/<str:partner_id>', api_open_close.TOpenClose.as_view()),
    path('setting/regular-holiday/<str:partner_id>', api_regular_holiday.TReqularHoliday.as_view()),
    path('setting/artist-vacation/<str:partner_id>', api_artist_vacation.TVacation.as_view()),
    path('setting/part-time/<str:partner_id>', api_part_time.TPartTime.as_view()),
    path('setting/break-time/<str:partner_id>', api_break_time.TBreakTime.as_view()),
    path('setting/artist-put', api_artist_setting.TAuthSetting.as_view()),
    path('setting/out-artist', api_artist_setting.TArtistOut.as_view()),
    path('setting/view-artist', api_artist_setting.TArtistView.as_view()),
    path('setting/ord-artist', api_artist_setting.TArtistOrd.as_view()),
    path('setting/is-authority', api_auth_setting.TAuthSetting.as_view()),
    path('setting/authority', api_auth_setting.TAuthSetting.as_view()),

]