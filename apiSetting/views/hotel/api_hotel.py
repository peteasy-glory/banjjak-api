# -*- coding: utf-8 -*-
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_HOTEL_GET, PROC_SETTING_HOTEL_PUT, PROC_SETTING_HOTEL_PUT_HOTELINFO
from hptopLib.TAPIIDBase import TAPIIDBase


class THotel(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_HOTEL_GET % (partner_id,), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(
                         PROC_SETTING_HOTEL_PUT % (args[1]["idx"],args[1]["is_pickup"],args[1]["is_24hour"],
                                                                                       args[1]["check_in"],args[1]["check_out"],
                                                                                       args[1]["is_coupon"],args[1]["is_flat"],
                                                                                       args[1]["pet_type"]),QUERY_DB)
            elif args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(
                        PROC_SETTING_HOTEL_PUT_HOTELINFO % (args[1]["idx"], args[1]["artist_id"],
                                                            args[1]["info_msg"]), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None

class THotelInfo(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        pass

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(
                    PROC_SETTING_HOTEL_PUT_HOTELINFO % (args[1]["idx"], args[1]["artist_id"],
                                                        args[1]["info_msg"]), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None

