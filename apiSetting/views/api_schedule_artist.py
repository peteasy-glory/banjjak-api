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
from hptopLib.TAPIIDBase import TAPIIDBase
from hptopLib.TAPISettingBase import TAPISettingBase


class TScheduleArtist(TAPIIDBase):
    """
    미용사 근무 일정.
    """

    # def getInfo(self, partner_id):
    #     working = TArtistWork()
    #     vacation = TVacation()
    #     break_time = TBreakTime()
    #     open_close = TOpenClose()
    #     regular_holiday = TReqularHoliday()
    #
    #     body = {}
    #     err, msg, body_working = working.getInfo(partner_id)
    #     if err < 0:
    #         return err, msg, body
    #     err, msg, body_vacation = vacation.getInfo(partner_id)
    #     if err < 0:
    #         return err, msg, body
    #     err, msg, body_break_time = break_time.getInfo(partner_id)
    #     if err < 0:
    #         return err, msg, body
    #     err, msg, body_open_close = open_close.getInfo(partner_id)
    #     if err < 0:
    #         return err, msg, body
    #     err, msg, body_reqular_holiday = regular_holiday.getInfo(partner_id)
    #     if err < 0:
    #         return err, msg, body
    #     body["working"] = body_working
    #     body["vacation"] = body_vacation
    #     body["break_time"] = body_break_time
    #     body["open_close"] = body_open_close
    #     body["regular_holiday"] = body_reqular_holiday
    #
    #     return err, msg, body

    def getInfo(self, partner_id, *args):
        try:
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

            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_VAT_PUT % (args[1]["partner_id"], args[1]["is_vat"]), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", {}
        except Exception as err:
            return -1, self.errorInfo(err), None
