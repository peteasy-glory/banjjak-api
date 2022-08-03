# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBookingBase import TAPIBookingBase


class TPaymentGoods(TAPIBookingBase):

    def getInfo(self, payment_idx, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PAYMENT_INFO_GET % (payment_idx,), QUERY_DB)
            body = {}
            if value is not None:
                body["origin"] = value[36]
                body["parsing"] = self.productToDic(value[36])
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None

    def putInfo(self, *args):
        pass
        # try:
        #     value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_NO_SHOW_PUT % (args[0]["payment_idx"],args[0]["is_no_show"]), QUERY_DB)
        #     body = {}
        #     if value is not None:
        #         body = self.queryDataToDic(value, rows, columns)
        #     return 0, "success", body
        # except Exception as e:
        #     return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None