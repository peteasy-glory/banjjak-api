# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_RESERVE_PAYMENT_PUT
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TPayment(TAPIBookingIDBase):

    def getInfo(self, partner_id, *args):
        try:
            pass
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            value = None
            row = None
            columns = None
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_RESERVE_PAYMENT_PUT % (args[1]["payment_log_seq"], args[1]["reserve_pay_yn"]), QUERY_DB)
            else:
                return -1, "undefined method", {}
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, traceback.format_exc(), None
