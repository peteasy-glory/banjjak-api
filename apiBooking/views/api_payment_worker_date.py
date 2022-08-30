# -*- coding: utf-8 -*-


from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBookingBase import TAPIBookingBase



class TWorkerDate(TAPIBookingBase):
    def getInfo(self, payment_idx, *args):
        try:
            pass
        except Exception as err:
            return -1, self.errorInfo(err), None

    def modifyInfo(self, *args):
        try:
            body = {}
            if args[1] == 'PUT':
                value, rows, columns = self.db.resultDBQuery(PROC_BEAUTY_BOOKING_DATE_WORKER_PUT % (args[0]["idx"]
                                                            , args[0]["st_date"], args[0]["fi_date"]
                                                             , args[0]["worker"]), QUERY_DB)
                if value is not None:
                    body = self.queryDataToDic(value, rows, columns)
                return 0, "success", body
            return - 1, "undefined method", body
        except Exception as err:
            return -1, self.errorInfo(err), None