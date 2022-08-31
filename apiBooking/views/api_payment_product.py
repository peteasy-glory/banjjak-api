# -*- coding: utf-8 -*-

import traceback
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_BEAUTY_PRODUCT_PUT, PROC_BEAUTY_BOOKING_COUPON_MODIFY
from hptopLib.TAPIBookingBase import TAPIBookingBase

class TPaymentProduct(TAPIBookingBase):

    def getInfo(self, payment_idx, *args):
        try:
            pass
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[1] == 'PUT':
                for c in args[0]["coupon"]:
                    value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_COUPON_MODIFY % (args[0]["payment_idx"],
                                                                                                        args[0]["tmp_user_idx"],
                                                                                                        args[0]["customer_id"],
                                                                                                        args[0]["partner_id"],
                                                                                                        c["idx"]), QUERY_DB)
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_BEAUTY_PRODUCT_PUT % (args[0]["payment_idx"],
                                                                                                    args[0]["use_coupon"],
                                                                                                    args[0]["price"],
                                                                                                    args[0]["product"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as e:
            return -1, traceback.format_exc(), None
