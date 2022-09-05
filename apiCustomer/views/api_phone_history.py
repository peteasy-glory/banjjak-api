# -*- coding: utf-8 -*-
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_CUSTOMER_SUB_PHONE_POST, PROC_CUSTOMER_SUB_PHONE_GET, PROC_CUSTOMER_SUB_PHONE_DELETE, \
    PROC_CUSTOMER_PHONE_CHANGE_HISTORY_GET, PROC_CUSTOMER_PHONE_CHANGE_HISTORY_POST
from hptopLib.TAPIIDBase import TAPIIDBase


class TMainPhone(TAPIIDBase):

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_PHONE_CHANGE_HISTORY_GET % (partner_id, args[0]["customer_id"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            if args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_PHONE_CHANGE_HISTORY_POST % (args[1]["partner_id"],
                                                                                             args[1]["customer_id"],
                                                                                             args[1]["tmp_user_idx"],
                                                                                             args[1]["old_phone"],
                                                                                             args[1]["new_phone"]), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", {}
        except Exception as err:
            return -1, self.errorInfo(err), None