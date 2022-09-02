# -*- coding: utf-8 -*-

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_CUSTOMER_RESERVES_GET
from hptopLib.TAPIIDBase import TAPIIDBase


class TReserves(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_RESERVES_GET % (args[0]["payment_idx"]
                                                                                       ,args[0]["customer_id"]
                                                                                       ,args[0]["tmp_user_idx"]
                                                                                       ,args[0]["service"]
                                                                                       ,args[0]["reserve_type"]), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None


    def modifyInfo(self, *args):
        pass

