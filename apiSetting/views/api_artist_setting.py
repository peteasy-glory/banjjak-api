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
                return HttpResponse(self.json.dicToJson(self.message.errorDBDuplicate()))
            elif data[1] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
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

    def delete(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["name"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            name = dic["name"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_THE_ARTIST_DEL % (artist_id, name), QUERY_DB)
            ret = self.message.successOk()
            print(data)
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 1:
                return HttpResponse(self.json.dicToJson(self.message.errorDBSelect()))
            elif data[1] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            else:
                for d in dic['work']:
                    value, rows1, columns1 = self.db.resultDBQuery(PROC_SETTING_ARTIST_POST % (artist_id, name, dic["nicname"], dic["is_main"], dic["is_out"], dic["is_view"], d['week'], d['time_st'], d['time_fi'], dic["sequ_prnt"]), QUERY_DB)
                    ret = self.message.successOk()
                    if value is None:
                        return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
                    if value[0] > 0:
                        return HttpResponse(self.json.dicToJson(self.message.errorDBDuplicate()))
                    elif value[1] < 0:
                        return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))
