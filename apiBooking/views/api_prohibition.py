# -*- coding: utf-8 -*-
import traceback

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import PROC_BEAUTY_BOOKING_PROHIBITION_GET, PROC_BEAUTY_BOOKING_PROHIBITION_POST, \
    PROC_BEAUTY_BOOKING_PROHIBITION_DELETE
from hptopLib.TAPIBookingIDBase import TAPIBookingIDBase


class TProhibition(TAPIBookingIDBase):

    def getInfo(self, payment_id, *args):
        try:
            if len(args) < 1:
                return -1, "Post Data를 확인해 주세요.", None
            else:
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PROHIBITION_GET % (payment_id,
                                                                                                    args[0]["st_date"],
                                                                                                    args[0]["fi_date"]), QUERY_DB)
                body = {}
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None


    def modifyInfo(self, *args):
        try:
            if args[0] == 'POST':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PROHIBITION_POST % (args[1]["partner_id"],
                                                                                                    args[1]["worker"],
                                                                                                    args[1]["type"],
                                                                                                    args[1]["st_date"],
                                                                                                    args[1]["fi_date"]), QUERY_DB)
            elif args[0] == 'DELETE':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_PROHIBITION_DELETE % (args[1]["idx"],), QUERY_DB)
            else:
                return -1, "no put method", None
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as err:
            return -1, traceback.format_exc(), None





