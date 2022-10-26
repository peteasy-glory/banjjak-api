# -*- coding: utf-8 -*-
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *
from hptopLib.TAPIBookingBase import TAPIBookingBase


class TNoShow(TAPIBookingBase):

    def modifyInfo(self, *args):
        try:
            if args[1] == 'PUT':
                body = {}
                if args[0]["payment_idx"] != 0 and args[0]["cellphone"] =='':
                    value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_NO_SHOW_PUT % (args[0]["payment_idx"],args[0]["is_no_show"]), QUERY_DB)
                    if value is not None:
                        body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
                elif args[0]["payment_idx"] == 0 and args[0]["cellphone"] !='' and args[0]["partner_id"] !='':
                    value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_NO_SHOW_ALL_PUT % (args[0]["partner_id"],args[0]["cellphone"],args[0]["is_no_show"]), QUERY_DB)
                    if value is not None:
                        body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
                else:
                    return -1, "post data 확인 해 주세요.", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, self.errorInfo(e), None

    def getInfo(self, payment_idx, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PAYMENT_INFO_GET % (payment_idx,), QUERY_DB)
            body = {}
            if value is not None:
                #body = self.queryDataToDic(value, rows, columns)
                body["is_no_show"] = zeroToBool(value[51])
            return 0, "success", body
        except Exception as e:
            return -1, self.errorInfo(e), None


class TNoShowHotel(TAPIBookingBase):

    def modifyInfo(self, *args):
        try:
            if args[1] == 'PUT':
                body = {}
                if args[0]["order_num"] != '' and args[0]["cellphone"] =='':
                    value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_NO_SHOW_HOTEL_PUT % (args[0]["order_num"],args[0]["is_no_show"]), QUERY_DB)
                    if value is not None:
                        body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
                elif args[0]["order_num"] == '' and args[0]["cellphone"] !='' and args[0]["partner_id"] !='':
                    value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_NO_SHOW_ALL_HOTEL_PUT % (args[0]["partner_id"],args[0]["cellphone"],args[0]["is_no_show"]), QUERY_DB)
                    if value is not None:
                        body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
                else:
                    return -1, "post data 확인 해 주세요.", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, self.errorInfo(e), None

    def getInfo(self, payment_idx, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PAYMENT_INFO_GET % (payment_idx,), QUERY_DB)
            body = {}
            if value is not None:
                #body = self.queryDataToDic(value, rows, columns)
                body["is_no_show"] = zeroToBool(value[51])
            return 0, "success", body
        except Exception as e:
            return -1, self.errorInfo(e), None

