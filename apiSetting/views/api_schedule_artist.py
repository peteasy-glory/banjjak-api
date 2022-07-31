# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiSetting.views.api_artist_vacation import TVacation
from apiSetting.views.api_artist_work import TArtistWork
from apiSetting.views.api_break_time import TBreakTime
from apiSetting.views.api_open_close import TOpenClose
from apiSetting.views.api_regular_holiday import TReqularHoliday
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TAPISettingBase import TAPISettingBase


class TScheduleArtist(TAPISettingBase):
    """
    미용사 근무 일정.
    """
    def __init__(self):
        pass

    def __del__(self):
        pass

    def getInfo(self, partner_id):
        working = TArtistWork()
        vacation = TVacation()
        break_time = TBreakTime()
        open_close = TOpenClose()
        regular_holiday = TReqularHoliday()

        body = {}
        err, msg, body_working = working.getInfo(partner_id)
        if err < 0:
            return err, msg, body
        err, msg, body_vacation = vacation.getInfo(partner_id)
        if err < 0:
            return err, msg, body
        err, msg, body_break_time = break_time.getInfo(partner_id)
        if err < 0:
            return err, msg, body
        err, msg, body_open_close = open_close.getInfo(partner_id)
        if err < 0:
            return err, msg, body
        err, msg, body_reqular_holiday = regular_holiday.getInfo(partner_id)
        if err < 0:
            return err, msg, body
        body["working"] = body_working
        body["vacation"] = body_vacation
        body["break_time"] = body_break_time
        body["open_close"] = body_open_close
        body["regular_holiday"] = body_reqular_holiday

        return err, msg, body


