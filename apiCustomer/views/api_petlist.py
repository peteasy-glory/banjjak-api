# -*- coding: utf-8 -*-

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_CUSTOMER_PET_LIST_GET, PROC_CUSTOMER_PET_DELETE
from hptopLib.TAPIIDBase import TAPIIDBase


class TPetList(TAPIIDBase):
    def getInfo(self, partner_id, *args):

        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_PET_LIST_GET % (partner_id,args[0]["cellphone"]), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'DELETE':
                body = {}
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_PET_DELETE % (args[1]["partner_id"],args[1]["pet_idx"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return -1, "undefined method", {}
        except Exception as e:
            return -1, self.errorInfo(e), None
