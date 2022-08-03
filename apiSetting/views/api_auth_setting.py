# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class TAuthSetting(TAPIBase):
    """
    미용사 권한 설정.
    """

    def __init__(self):
        pass

    def __del__(self):
        pass

    def get(self, request, partner_id):
        try:
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            err, body = self.getArtistList(partner_id)
            ret = self.message.successOk()
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def post(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["name"] is None or dic["week"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            name = dic["name"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_POST % (artist_id,name,dic["nicname"],dic["is_main"],dic["is_out"],dic["is_view"],dic["week"],dic["time_start"],dic["time_end"],dic["sequ_prnt"]), QUERY_DB)
            ret = self.message.successOk()
            print(data)
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] > 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            elif data[1] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBQuery()))
            # body = self.queryDataToSimpleDic((data[0],), rows, ["idx"])
            # ret["body"] = body
            # print(data)
            # print(data[0])
            # print(data[1])
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))

    def put(self, request):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))
