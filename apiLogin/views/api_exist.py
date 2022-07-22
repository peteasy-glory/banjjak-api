# -*- coding: utf-8 -*-
from django.http import HttpResponse
from apiShare.constVar import QUERY_DB
from apiShare.sqlQuery import *
from hptopLib.TAPIBase import TAPIBase

class TPhone(TAPIBase):
    def get(self, request, phone):
        try:
            if phone is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            data, rows, columns = self.db.resultDBQuery(PROC_IS_EXIST_PHONE_GET % (phone.strip(),), QUERY_DB)
            ret = self.message.successOk()
            body = {}
            if data is None or data[0] > 0:
                if data[0] > 0:
                    body["exist"] = True
                    body["message"] = "사용 할 수 없는 전화번호 입니다"
                else:
                    return HttpResponse(self.json.dicToJson(self.message.loginIdFail()))
            else:
                body["exist"] = False
                body["message"] = "사용 가능한 전화번호 입니다"
            ret["body"] =  body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))

class TEmail(TAPIBase):
    def get(self, request, email):
        try:
            if email is None:
                return HttpResponse(self.json.dicToJson(self.message.errorBadRequst()))
            data, rows, columns = self.db.resultDBQuery(PROC_IS_EXIST_ID_GET % (email.strip(),), QUERY_DB)
            ret = self.message.successOk()
            body = {}
            if data is None or data[0] > 0:
                if data[0] > 0:
                    body["exist"] = True
                    body["message"] = "사용 할 수 없는 이메일 입니다"
                else:
                    return HttpResponse(self.json.dicToJson(self.message.loginIdFail()))
            else:
                body["exist"] = False
                body["message"] = "사용 가능한 이메일 입니다"
            ret["body"] =  body
            return HttpResponse(self.json.dicToJson(ret))
        except Exception as e:
            return HttpResponse(self.json.dicToJson(self.message.error(e.args[0])))


