# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class TPayType(TAPIBase):
    """
    결제방식 설정
    """

    def get(self, request, partner_id):
        try:
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_PAY_TYPE_GET % (partner_id), QUERY_DB)
            if data is not None:
                return HttpResponse(self.json.dicToJson(data[0]))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def put(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["pay_type"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_PAY_TYPE_PUT % (artist_id, dic["pay_type"]),QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))


