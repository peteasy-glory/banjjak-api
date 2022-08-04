# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *
from hptopLib.TAPIBookingBase import TAPIBookingBase



class TShopGrade(TAPIBookingBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GRADE_SHOP_ID_GET % (partner_id,), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                #body["is_no_show"] = zeroToBool(value[51])
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None

    def putInfo(self, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_NO_SHOW_PUT % (args[0]["payment_idx"],args[0]["is_no_show"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None


class TCustomerGrade(TAPIBookingBase):

    def getInfo(self, customer_grade_idx, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PAYMENT_INFO_GET % (customer_grade_idx,), QUERY_DB)
            body = {}
            if value is not None:
                #body = self.queryDataToDic(value, rows, columns)
                body["is_no_show"] = zeroToBool(value[51])
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None

    def putInfo(self, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_NO_SHOW_PUT % (args[0]["payment_idx"],args[0]["is_no_show"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None