# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import PROC_CUSTOMER_BEAUTY_TOTAL_SEARCH_GET, PROC_CUSTOMER_KINDER_TOTAL_SEARCH_GET, \
    PROC_CUSTOMER_HOTEL_TOTAL_SEARCH_GET, PROC_CUSTOMER_TOTAL_COUNT_GET, PROC_ANIMAL_TOTAL_COUNT_GET
from hptopLib.TAPICustomerBase import TAPICustomerBase


class TTotalSearch(TAPICustomerBase):

    def getInfo(self, payment_id, *args):
        try:
            if args[0] == "beauty":
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_BEAUTY_TOTAL_SEARCH_GET % (payment_id, args[1]), QUERY_DB)
            elif args[0] == "hotel":
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_HOTEL_TOTAL_SEARCH_GET % (payment_id, args[1]),QUERY_DB)
            elif args[0] == "kinder":
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_KINDER_TOTAL_SEARCH_GET % (payment_id, args[1]),QUERY_DB)
            elif args[0] == "people":
                value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_TOTAL_COUNT_GET % (payment_id), QUERY_DB)
            elif args[0] == "animal":
                value, rows, columns = self.db.resultDBQuery(PROC_ANIMAL_TOTAL_COUNT_GET % (payment_id),QUERY_DB)
            body = {}
            if value is not None:
                if args[0] in ("beauty", "hotel", "kinder"):
                    body = self.queryDataToDic(value, rows, columns, ord = True)
                else:
                    body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None


