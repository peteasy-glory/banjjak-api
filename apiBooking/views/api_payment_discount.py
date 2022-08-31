# -*- coding: utf-8 -*-

import traceback
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_BEAUTY_DISCOUNT_PUT
from hptopLib.TAPIBookingBase import TAPIBookingBase

class TPaymentDiscount(TAPIBookingBase):

    def getInfo(self, payment_idx, *args):
        try:
            pass
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEAUTY_DISCOUNT_PUT % (args[0]["payment_idx"],
                                                                                                    args[0]["type"],
                                                                                                    args[0]["discount"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as e:
            return -1, traceback.format_exc(), None