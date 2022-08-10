# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class TReserve(TAPIBase):
    """
    적립금 설정
    """

    def get(self, request, partner_id):
        try:
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_RESERVE_GET % (partner_id), QUERY_DB)
            if data is not None:
                tmp = {}
                tmp["idx"] = data[0]
                tmp["artist_id"] = data[1]
                tmp["is_use"] = data[2]
                tmp["percent"] = data[3]
                tmp["min_reserve"] = data[4]
                tmp["is_delete"] = data[7]

            return HttpResponse(self.json.dicToJson(tmp))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def put(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["percent"] is None or dic["min_reserve"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_RESERVE_PUT % (artist_id, dic["is_use"], dic["percent"], dic["min_reserve"], dic["is_delete"]),QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))


