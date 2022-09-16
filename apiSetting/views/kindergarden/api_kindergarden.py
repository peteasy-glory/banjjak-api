# -*- coding: utf-8 -*-
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_SETTING_KINDERGARDEN_GET, PROC_SETTING_KINDERGARDEN_PUT
from hptopLib.TAPIIDBase import TAPIIDBase


class TKindergarden(TAPIIDBase):
    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_SETTING_KINDERGARDEN_GET % (partner_id,), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_SETTING_KINDERGARDEN_PUT % (args[1]["idx"],args[1]["is_pickup"],args[1]["is_neutral"],
                                                                                       args[1]["is_neutral_pay"],args[1]["neutral_price"],
                                                                                       args[1]["extra_price"],args[1]["is_coupon"],args[1]["is_flat"],
                                                                                       args[1]["is_weight"]),QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                    return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None