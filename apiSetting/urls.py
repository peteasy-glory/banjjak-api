# -*- coding: utf-8 -*-

from django.urls import path
from apiSetting.views import api_auth, api_open_close, api_regular_holiday, api_artist_vacation, api_part_time, \
    api_break_time
from apiSetting.views import api_auth, api_schedule_setting


urlpatterns = [

    path('schedule/artist-work/<str:partner_id>', api_schedule_setting.TArtistWork.as_view()),

    path('auth/artist/<str:partner_id>', api_auth.TAuthSetting.as_view()),
    path('auth/open-close/<str:partner_id>', api_open_close.TOpenClose.as_view()),
    path('auth/regular-holiday/<str:partner_id>', api_regular_holiday.TReqularHoliday.as_view()),
    path('auth/artist-vacation/<str:partner_id>', api_artist_vacation.TVacation.as_view()),
    path('auth/part-time/<str:partner_id>', api_part_time.TPartTime.as_view()),
    path('auth/break-time/<str:partner_id>', api_break_time.TBreakTime.as_view()),

    path('auth/artist', api_auth.TAuthSetting.as_view()),

    # path('pet/<str:owner_id>/<int:year>/<int:month>', api_log.TPetLogMonth.as_view()),
    # path('pets/<str:owner_id>', api_log.TPet.as_view()),
    # path('pet/<int:pet_id>', api_log.TPetLogInfo.as_view()),
    # path('year/<str:owner_id>/<int:pet_id>/<int:year>', api_log.TPetIndividualLogYear.as_view()),
    # path('month/<str:owner_id>/<int:pet_id>/<int:year>/<int:month>', api_log.TPetIndividualLogMonth.as_view()),
    # path('graph/<str:owner_id>/<int:year>/<int:month>', api_log.TPetLogGraph.as_view()),
    # path('photo/<str:owner_id>/<int:pet_id>/<int:year>/<int:month>', api_log.TPetIndividualLogMonthPhoto.as_view()),

]