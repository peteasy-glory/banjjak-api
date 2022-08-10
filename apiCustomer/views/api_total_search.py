# -*- coding: utf-8 -*-
from inspect import getframeinfo, currentframe

from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.funcLib import zeroToBool
from apiShare.sqlQuery import PROC_CUSTOMER_BEAUTY_TOTAL_SEARCH_GET, PROC_CUSTOMER_KINDER_TOTAL_SEARCH_GET, \
    PROC_CUSTOMER_HOTEL_TOTAL_SEARCH_GET, PROC_CUSTOMER_TOTAL_COUNT_GET, PROC_ANIMAL_TOTAL_COUNT_GET, \
    PROC_CUSTOMER_JOIN_POST
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

    def modifyInfo(self, *args):
        try:
            is_ok = True
            keys = ("partner_id","cellphone","name", "type", "pet_type","year","month","day","gender","neutral","weight","beauty_exp","vaccination","bite","luxation","dermatosis", "heart_trouble","marking", "mounting","memo")
            for key in keys:
                if not (key in args[0]):
                    return 408, "Post Data를 확인해 주세요.", {}
            value, rows, columns = self.db.resultDBQuery(PROC_CUSTOMER_JOIN_POST % (
                    args[0]["partner_id"], args[0]["cellphone"], args[0]["name"], args[0]["type"]
                    , args[0]["pet_type"], args[0]["year"], args[0]["month"], args[0]["day"]
                    , args[0]["gender"], args[0]["neutral"], args[0]["weight"], args[0]["beauty_exp"]
                    , args[0]["vaccination"], args[0]["bite"], args[0]["luxation"], args[0]["dermatosis"]
                    , args[0]["heart_trouble"], args[0]["marking"], args[0]["mounting"], args[0]["memo"]), QUERY_DB)
            body = {}
            if value is not None:
                body = self.queryDataToDic(value, rows, columns)
            return 0, "success", body
        except Exception as e:
            return -1, self.frameInfo(getframeinfo(currentframe()), e.args[0]), None



