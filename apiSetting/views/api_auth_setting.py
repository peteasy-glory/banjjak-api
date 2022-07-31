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
            err, msg, body = self.getArtistWorkInfo(partner_id)
            if err == 0:
                ret = self.message.successOk()
                ret["body"] = body
                return HttpResponse(self.json.dicToJson(ret))
            else:
                return HttpResponse(self.json.dicToJson(self.message.error(msg)))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    # def get(self, request, year, month, partner_id):
    #     try:
    #         if partner_id is None:
    #             return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
    #         data, rows, columns = self.db.resultDBQuery(PROC_SHOP_NAME_GET % (partner_id), QUERY_DB)
    #         ret = self.message.successOk()
    #         if data is None:
    #             ret["body"] = {}
    #             return HttpResponse(self.json.dicToJson(ret))
    #         body = self.queryDataToDic(data, rows, columns)
    #         ret["body"] = body
    #         return HttpResponse(self.json.dicToJson(ret))
    #     except Exception as e:
    #         print(e)
    #         return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))


    def post(self, request):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))

    def put(self, request):
        try:
            pass
        except Exception as e:
            print(e)
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[1])))
