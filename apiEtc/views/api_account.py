# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_ETC_RESIGN_PUT, PROC_ETC_PASSWORD_GET, PROC_ETC_PASSWORD_PUT
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase
from hptopLib.TSha256 import TSha256


class TPassword(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_ETC_PASSWORD_GET % (partner_id,),QUERY_DB)

            sha256 = TSha256()
            pw = sha256.strToShaDigestBase64Encode(args[0]["pw"].strip())
            if value is not None:
                if value[0] == pw:
                    body = {"is_same": True}
                else:
                    body = {"is_same": False}
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                sha256 = TSha256()
                pw = sha256.strToShaDigestBase64Encode(args[1]["pw"].strip())
                value, rows, columns = self.db.resultDBQuery(PROC_ETC_PASSWORD_PUT % (args[1]["partner_id"], pw), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                else:
                    body = {"err": -1}
                return 0, "success", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, traceback.format_exc(), None

class TNewPassword(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        pass

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                body = {}
                sha256 = TSha256()
                pw = sha256.strToShaDigestBase64Encode(args[1]["old_pw"].strip())
                value, rows, columns = self.db.resultDBQuery(PROC_ETC_PASSWORD_GET % (args[1]["partner_id"],), QUERY_DB)
                if value is not None:
                    if value[0] == pw:
                        pw = sha256.strToShaDigestBase64Encode(args[1]["new_pw"].strip())
                        value, rows, columns = self.db.resultDBQuery(
                            PROC_ETC_PASSWORD_PUT % (args[1]["partner_id"], pw), QUERY_DB)
                        if value is not None:
                            body = self.queryDataToDic(value, rows, columns)
                        else:
                            body = {"err": -1}
                        return 0, "success", body
                    else:
                        body = {"is_same": False}
                return 0, "success", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, traceback.format_exc(), None


class TResign(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            pass
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_ETC_RESIGN_PUT % (args[1]["partner_id"],), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                else:
                    body = {"err": -1}
                return 0, "success", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, traceback.format_exc(), None