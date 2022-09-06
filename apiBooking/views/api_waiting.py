# -*- coding: utf-8 -*-
import traceback

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_WAITING_LIST_GET, PROC_BEAUTY_BOOKING_WAITING_DECISION_PUT
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TBookingWaiting(TAPIBookingIDBase):

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_WAITING_DECISION_PUT %
                                                             (args[1]["approve_idx"],args[1]["decision_code"],args[1]["payment_idx"]),
                                                             QUERY_DB)
                return 0, "success", self.queryDataToDic(value, rows, columns)
        except Exception as err:
            return -1, traceback.format_exc(), None

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_WAITING_LIST_GET % (partner_id,), QUERY_DB)
            if value is None:
                return 0, "success", {}
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
