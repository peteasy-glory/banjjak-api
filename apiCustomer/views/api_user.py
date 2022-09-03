# -*- coding: utf-8 -*-

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_CUSTOMER_DELETE
from hptopLib.TAPIIDBase import TAPIIDBase


class TUser(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        pass

    def modifyInfo(self, *args):
        try:
            if args[0] == 'DELETE':
                body = {}
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_DELETE % (args[1]["partner_id"],args[1]["cellphone"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, self.errorInfo(e), None