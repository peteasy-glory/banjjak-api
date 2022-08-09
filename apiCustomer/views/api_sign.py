# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_CUSTOMER_BEAUTY_AGREE_GET
from hptopLib.TAPICustomerBase import TAPICustomerBase


class TSign(TAPICustomerBase):

    def getInfo(self, payment_id, *args):
        try:
            if args[0] == "beauty":
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_BEAUTY_AGREE_GET % (payment_id, args[1]), QUERY_DB)
            elif args[0] == "hotel":
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_BEAUTY_AGREE_GET % (payment_id, args[1]), QUERY_DB)
            elif args[0] == "kinder":
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_BEAUTY_AGREE_GET % (payment_id, args[1]), QUERY_DB)
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            else:
                body = {}
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None