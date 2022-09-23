# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_CUSTOMER_UNIQUE_MEMO_GET
from hptopLib.TAPIIDBase import TAPIIDBase


class TUniqueMemo(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_UNIQUE_MEMO_GET % (partner_id,args[0]["pet_seq"]), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        pass
