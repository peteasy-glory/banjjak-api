# -*- coding: utf-8 -*-


from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBookingBase import TAPIBookingBase


class TMemo(TAPIBookingBase):
    def getInfo(self, payment_idx, *args):
        try:
            pass
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PAYMENT_MEMO_PUT % (args[0]["idx"]
                                                            , args[0]["memo"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None


class TMemoHotel(TAPIBookingBase):
    def getInfo(self, payment_idx, *args):
        try:
            pass
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PAYMENT_MEMO_HOTEL_PUT % (args[0]["order_num"]
                                                            , args[0]["memo"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None