# -*- coding: utf-8 -*-
from curses.ascii import isdigit
from inspect import getframeinfo, currentframe
from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import *
from hptopLib.TAPIBooking import TAPIBooking
from hptopLib.TAPIBookingBase import TAPIBookingBase
from hptopLib.TAPIIDBase import TAPIIDBase


class TShopGrade(TAPIBooking):

    def getInfo(self, *args):
        try:
            if type(args[0]["arg"]) == str:
                if args[0]["arg"].isdigit():
                    value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GRADE_SHOP_IDX_GET % (int(args[0]["arg"]),),QUERY_DB)
                else:
                    value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GRADE_SHOP_ID_GET % (args[0]["arg"],), QUERY_DB)
            else:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GRADE_SHOP_IDX_GET % (args[0]["arg"],), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None

    def modifyInfo(self, *args):
        try:
            if "customer_id" in args[0] and "grade_idx" in args[0]:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GRADE_CUSTOMER_POST % (0, args[0]["grade_idx"],args[0]["customer_id"]), QUERY_DB)
            elif "customer_idx" in args[0] and "grade_idx" in args[0]:
                value, rows, columns = self.db.resultDBQuery(
                    PROC_BEAUTY_BOOKING_GRADE_CUSTOMER_POST % (args[0]["customer_idx"], args[0]["grade_idx"], ""), QUERY_DB)
            else:
                return -1, "post data를 확인 해주세요.", None
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None


class TGrade(TAPIIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GRADE_CUSTOMER_GET % (partner_id, args[0]["cellphone"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_GRADE_SHOP_PUT % (args[1]["grade_idx"], args[1]["new_name"]), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", {}
        except Exception as err:
            return -1, self.errorInfo(err), None