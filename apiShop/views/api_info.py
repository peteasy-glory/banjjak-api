# -*- coding: utf-8 -*-
import traceback
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SHOP_INFO_BASE_GET, PROC_SHOP_INFO_LICENSE_AWARD_GET, PROC_SHOP_INFO_SALES_AREA_GET, \
    PROC_SHOP_INFO_AREA_ADDR_GET, PROC_SHOP_INFO_SALES_AREA_DELETE, PROC_SHOP_INFO_SALES_AREA_POST, \
    PROC_SHOP_INFO_LICENSE_AWARD_DELETE, PROC_SHOP_INFO_LICENSE_AWARD_POST
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase
from hptopLib.TDate import TDate
from hptopLib.TS3 import TS3


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
            value = None
            rows = None
            columns = None
            if args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_SALES_AREA_DELETE % (args[1]["partner_id"],
                                                                                                 args[1]["region_id"]),
                                                             QUERY_DB)
            elif args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_SALES_AREA_POST % (args[1]["partner_id"],
                                                                                                 args[1]["region_id"]),
                                                             QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            else:
                body = {"err": -1}
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

class TAreaAddr(TAPIBookingIDBase):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_AREA_ADDR_GET % (args[0]["addr_first"],
                                                                                         args[0]["addr_middle"]),
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
            value = None
            rows = None
            columns = None
            if args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_LICENSE_AWARD_DELETE % (args[1]["partner_id"],
                                                                                                 args[1]["type"],args[1]["photo"]),
                                                             QUERY_DB)
            elif args[0] == 'POST':
                date = TDate()
                fName = "customer_photo_" + date.customDateTime(format_date="%Y%m%d%H%M%S%f") + "." + args[1]["mine"]
                s3 = TS3()
                err, msg = s3.frontUpload(args[1]["partner_id"], file_name=fName, origin_file=args[1]["image"])
                body = {}
                if err == -1:
                    return -1, "Fail image uplad", body
                value, rows, columns = self.db.resultDBQuery(PROC_SHOP_INFO_LICENSE_AWARD_POST % (args[1]["partner_id"],
                                                                                                 args[1]["type"],args[1]["name"],
                                                                                                 args[1]["issued_by"],
                                                                                                 args[1]["published_date"],msg),
                                                             QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            else:
                body = {"err": -1}
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None
