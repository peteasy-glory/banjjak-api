# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class TArtistWork(TAPIBase):
    """
    미용사 근무 일정.
    """

    def __init__(self):
        pass

    def __del__(self):
        pass

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_WORKING_GET % (partner_id,), QUERY_DB)
            ret = self.message.successOk()
            body = {}
            if data is not None:
                body = {"open": data[1], "close": data[2], "is_work_holiday":True if data[3] == 0 else False }
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_SHOP_OPEN_CLOSE_GET % (partner_id,), QUERY_DB)
            if data is not None:
                body["reqular_holiday"] = str(data[1])+str(data[2])+str(data[3])+str(data[4])\
                                                        +str(data[5])+str(data[6])+str(data[7])
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))