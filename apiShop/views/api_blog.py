# -*- coding: utf-8 -*-
import traceback
from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_SHOP_WORKING_TIME_GET, PROC_BEAUTY_BOOKING_STATUTORY_HOLIDAYS_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TBlog(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_STATUTORY_HOLIDAYS_GET % (args[0]["year"],args[0]["month"],),
                                                         QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            pass
        except Exception as err:
            return -1, traceback.format_exc(), None