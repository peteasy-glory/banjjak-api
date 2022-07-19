# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TSha256 import TSha256


class TLogin(TAPIBase):
    def get(self, request):
        try:
            dic = request.data
            if dic["id"] is None or dic["pw"] is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            data, rows, columns = self.db.resultDBQuery(PROC_LOGIN_GET % (dic["id"].strip(),), QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))
            sha256 = TSha256()
            pw = sha256.strToShaDigestBase64Encode(dic["pw"].strip())
            if data[1] != pw:
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))

            body = self.queryDataToDic(data, rows, columns)
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))