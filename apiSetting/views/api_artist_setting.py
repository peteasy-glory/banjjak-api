# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase


class TAuthSetting(TAPIBase):
    """
    미용사 등록 및 수정.
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
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))

    def put(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["name"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            name = dic["name"].strip()
            for d in dic['work']:
                data, rows1, columns1 = self.db.resultDBQuery(PROC_SETTING_ARTIST_PUT % (artist_id, name, dic["nicname"], dic["is_main"], dic["is_out"], dic["is_view"], d['is_work'], d['week'], d['time_st'], d['time_fi'], dic["sequ_prnt"]), QUERY_DB)
                ret = self.message.successOk()
                if data is None:
                    return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
                if data[0] > 0:
                    return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))
                elif data[1] < 0:
                    return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def delete(self, request):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))


class TArtistOut(TAPIBase):
    """
    미용사 퇴사 설정.
    """

    def put(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["name"] is None or dic["is_out"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            name = dic["name"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_OUT_PUT % (artist_id, name, dic["is_out"]), QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))


class TArtistView(TAPIBase):
    """
    미용사 숨김 설정.
    """

    def put(self, request):
        try:
            dic = request.data

            if dic["artist_id"] is None or dic["name"] is None or dic["is_view"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            artist_id = dic["artist_id"].strip()
            name = dic["name"].strip()
            data, rows, columns = self.db.resultDBQuery(PROC_SETTING_ARTIST_VIEW_PUT % (artist_id, name, dic["is_view"]), QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.errorDBInsert()))
            if data[0] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBUpdate()))

            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))
