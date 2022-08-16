# -*- coding: utf-8 -*-
import traceback

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_WAITING_LIST_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TBookingWaiting(TAPIBookingIDBase):

    def modifyInfo(self, *args):
        pass

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_WAITING_LIST_GET % (partner_id,), QUERY_DB)
            ret = self.message.successOk()
            if value is None:
                ret["body"] = {}
                return ret
            data = []
            body = []
            if rows < 2:
                data.append(value)
            else:
                data = value
            for d in data:
                body.append(self.setBeautyData(d))
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None
