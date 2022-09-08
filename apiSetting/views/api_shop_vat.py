# -*- coding: utf-8 -*-

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_SHOP_VAT_PUT, PROC_SETTING_SHOP_VAT_GET
from hptopLib.TAPIIDBase import TAPIIDBase


class TShopVat(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            body = {}
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_SHOP_VAT_GET % (partner_id,),QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if  args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_SHOP_VAT_PUT % (args[1]["partner_id"],
                                                            args[1]["is_vat"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None
