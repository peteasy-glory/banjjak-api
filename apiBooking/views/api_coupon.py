# -*- coding: utf-8 -*-

import traceback
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_COUPON_GET, PROC_BEAUTY_BOOKING_CUTOMER_COUPON_GET
from hptopLib.TAPIIDBase import TAPIIDBase

class TCoupon(TAPIIDBase):

    def getInfo(self, partner_id, *args):
        try:
            if "type" in args[0]:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_COUPON_GET % (partner_id,
                                                                                                  args[0]["type"],
                                                                                                  args[0]["coupon_type"]), QUERY_DB)
            else:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_CUTOMER_COUPON_GET % (partner_id,
                                                                                                  args[0]["customer_id"],
                                                                                                  args[0]["tmp_user_idx"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None

    def modifyInfo(self, *args):
        try:
            pass
        except Exception as e:
            return -1, traceback.format_exc(), None