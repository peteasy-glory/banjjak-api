# -*- coding: utf-8 -*-
from django.http import HttpResponse

from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase
from hptopLib.TSha256 import TSha256
import random

class TJoin(TAPIBase):
    def get (self, request, partner_id):
        try:
            dic = request.data
            if partner_id is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            data, rows, columns = self.db.resultDBQuery(PROC_ID_GET % (partner_id.strip(),), QUERY_DB)
            ret = self.message.successOk()
            body = {}
            if data is None or data[0] > 0:
                if data[0] > 0:
                    body["message"] = "사용 할 수 없는 아이디입니다"
                else:
                    return HttpResponse(self.json.dicToJson(self.message.loginIdFail()))
            else:
                body["message"] = "사용 가능한 아이디입니다"
            ret["body"] =  body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))


    def post(self, request):
        try:
            dic = request.data
            if dic["id"] is None or dic["pw"] is None or dic["phone"] is None :
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))

            sha256 = TSha256()
            pw = sha256.strToShaDigestBase64Encode(dic["pw"].strip())
            id = dic["id"].strip()
            id_pos = id.find("@")
            if id_pos > 5:
                nick = id.split("@")[0][:-3] + ("_%06d" % random.randint(000000, 999999))
            else:
                nick = id.split("@")[0] + ("_%06d" % random.randint(000000, 999999))
            data, rows, columns = self.db.resultDBQuery(PROC_JOIN_POST % (id,pw,nick,dic["phone"]), QUERY_DB)
            ret = self.message.successOk()
            if data is None:
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))
            if data[0] > 0:
                return HttpResponse(self.json.dicToJson(self.message.loginFail()))
            elif data[1] < 0:
                return HttpResponse(self.json.dicToJson(self.message.errorDBQuery()))
            body = self.queryDataToSimpleDic((data[0],), rows, ["idx"])
            ret["body"] = body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))