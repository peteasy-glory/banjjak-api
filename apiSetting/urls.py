# -*- coding: utf-8 -*-

from django.urls import path
from apiSetting.views import api_auth_setting
from apiSetting.views import api_auth_setting, api_schedule_setting


urlpatterns = [

    path('schedule/artist-work/<str:partner_id>', api_schedule_setting.TArtistWork.as_view()),

    path('auth/artist/<str:partner_id>', api_auth_setting.TAuthSetting.as_view()),
    path('auth/artist', api_auth_setting.TAuthSetting.as_view()),

    # path('pet/<str:owner_id>/<int:year>/<int:month>', api_log.TPetLogMonth.as_view()),
    # path('pets/<str:owner_id>', api_log.TPet.as_view()),
    # path('pet/<int:pet_id>', api_log.TPetLogInfo.as_view()),
    # path('year/<str:owner_id>/<int:pet_id>/<int:year>', api_log.TPetIndividualLogYear.as_view()),
    # path('month/<str:owner_id>/<int:pet_id>/<int:year>/<int:month>', api_log.TPetIndividualLogMonth.as_view()),
    # path('graph/<str:owner_id>/<int:year>/<int:month>', api_log.TPetLogGraph.as_view()),
    # path('photo/<str:owner_id>/<int:pet_id>/<int:year>/<int:month>', api_log.TPetIndividualLogMonthPhoto.as_view()),

]