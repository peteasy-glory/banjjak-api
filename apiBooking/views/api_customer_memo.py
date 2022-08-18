
# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_CUSTOMER_MEMO_PUT, PROC_BEAUTY_BOOKING_CUSTOMER_MEMO_GET
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TCustomerMemo(TAPIBookingIDBase):

    def modifyInfo(self, *args):
        try:
            if args[0] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_CUSTOMER_MEMO_PUT %
                                                             (args[1]["idx"],args[1]["memo"]),
                                                             QUERY_DB)
                return 0, "success", self.queryDataToDic(value, rows, columns)
        except Exception as err:
            return -1, traceback.format_exc(), None

    def getInfo(self, partner_id, *args):
        try:
            value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_CUSTOMER_MEMO_GET %
                                    (partner_id, args[0]["customer_id"], args[0]["tmp_seq"], args[0]["cellphone"]), QUERY_DB)
            return 0, "success", self.queryDataToDic(value, rows, columns)
        except Exception as err:
            return -1, traceback.format_exc(), None