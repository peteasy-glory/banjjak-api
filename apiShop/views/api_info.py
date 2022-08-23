# -*- coding: utf-8 -*-
import traceback
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SHOP_INFO_BASE_GET, PROC_SHOP_INFO_LICENSE_AWARD_GET, PROC_SHOP_INFO_SALES_AREA_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TInfo(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_BASE_GET % (partner_id,),
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


class TSalesArea(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_SALES_AREA_GET % (partner_id,),
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


class TLicenseAward(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_LICENSE_AWARD_GET % (partner_id,args[0]["type"]),
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
