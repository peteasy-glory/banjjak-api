# -*- coding: utf-8 -*-
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_VAT_GET, PROC_SETTING_VAT_PUT
from hptopLib.TAPIIDBase import TAPIIDBase


class TAPIVat(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_VAT_GET % (partner_id,), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_VAT_PUT % (args[1]["partner_id"], args[1]["is_vat"]), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", {}
        except Exception as err:
            return -1, self.errorInfo(err), None